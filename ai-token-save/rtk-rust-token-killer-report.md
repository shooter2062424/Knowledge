# RTK (Rust Token Killer) — Detailed Study Report

**Topic:** AI / Token-Saving Developer Tooling
**Subject repository:** [rtk-ai/rtk](https://github.com/rtk-ai/rtk)
**Project site:** https://www.rtk-ai.app/
**Date of study:** 2026-05-22

---

## 1. Executive Summary

RTK ("Rust Token Killer") is an open-source command-line **proxy** that sits between an AI coding
assistant and the shell. When an agent runs ordinary developer commands (`git status`, `cargo test`,
`grep`, `npm install`, …), RTK runs the real command, then **filters and compresses the output**
before it is returned to the model's context window.

The headline claim is a **60–90% reduction in LLM token consumption** on common dev commands,
delivered as a **single Rust binary with zero runtime dependencies** and **<10 ms overhead** per
invocation. In a representative 30-minute Claude Code session on a mixed TypeScript/Rust project, the
project reports a drop from **~118,000 tokens to ~23,900 tokens (~80% overall reduction)**.

The core insight: most CLI output is *noise* to an LLM (boilerplate, progress bars, repeated lines,
passing-test logs, whitespace). Stripping that noise both **cuts API cost** and **extends the usable
context window**, allowing longer agent sessions before compaction.

---

## 2. The Problem It Solves

AI coding agents work by reading terminal output and feeding it back into the model's context. Raw
command output is verbose and largely irrelevant to the model's decision:

- A test suite prints thousands of lines, but the agent only needs the **failures**.
- `git status` / `git diff` emit large blocks where only the **changed paths or hunks** matter.
- `ls`, `find`, `grep` can return huge lists with massive redundancy.
- Build/lint tools emit progress, timing, and success spam around the few **error lines** that count.

Every one of those lines costs tokens twice over: once on input (the model reads it) and indirectly by
crowding out the context window, forcing earlier truncation/compaction. RTK's thesis is that a
deterministic, command-aware filter can remove ~89% of this noise without losing the signal the agent
actually needs.

---

## 3. How It Works (Architecture)

### 3.1 Command proxy pattern
RTK is structured as a **command proxy**. `main.rs` parses the invocation with **Clap** and routes it
through a `Commands` enum to a **specialized filter module** for that tool/ecosystem. Each filter:

1. Executes the underlying real command (e.g. shells out to `cargo test`).
2. Captures stdout/stderr.
3. Runs the output through a **compression pipeline**.
4. Returns the compacted result to the caller (the agent).

### 3.2 The filtering pipeline
Four core strategies are applied (per command, tuned to that command's output shape):

| Strategy        | What it does                                                        |
|-----------------|---------------------------------------------------------------------|
| Smart filtering | Drops noise lines (progress, timestamps, passing cases, banners).   |
| Grouping        | Aggregates similar/related items into a compact summary.            |
| Truncation      | Keeps the most relevant context, trims the long tail.               |
| Deduplication   | Collapses repeated/identical lines.                                 |

### 3.3 Fallback & "tee" safety
- **Fallback pattern:** if filtering fails for any reason, the *raw* command output is returned
  unchanged — RTK should never break a workflow, only slim it.
- **Tee on failure:** full unfiltered output can be saved to disk on failures so the agent (or human)
  can review the complete log when something actually breaks. This is a configurable "tee" mode.

### 3.4 Transparent auto-rewrite hook
The most important UX feature. Running:

```
rtk init --global      # or: rtk init -g
```

installs a **PreToolUse hook** in the agent (Claude Code / Copilot by default). The hook
**transparently rewrites** Bash commands to their `rtk` equivalents *before* execution
(`git status` → `rtk git status`, etc.). The agent keeps issuing normal commands; RTK intercepts and
compresses the output. The project describes this as achieving "100% RTK adoption" with no behavior
change required from the model.

> **Caveat:** Claude Code's *built-in* tools (Read, Grep, Glob) bypass the Bash hook. To get savings
> on those workflows the agent must explicitly call `rtk read` / `rtk grep`, or be steered to use the
> shell.

### 3.5 Metrics / tracking
A **SQLite-based tracking** layer (`src/core/tracking.rs`) records token-savings metrics so the user
can see realized gains via the `rtk gain` command.

---

## 4. Source Layout

```
src/
├── main.rs               # Clap entrypoint; routes Commands enum → filter modules
├── core/
│   └── tracking.rs       # SQLite token-savings metrics
└── cmds/                 # one folder per ecosystem; each has its own README + //! docs
    ├── system/           # ls, tree, grep, find, wc, env, json, log, deps  (language-agnostic)
    ├── git/              # git, gh (GitHub CLI), gt (Graphite), diff utilities
    ├── rust/             # cargo, test/error runner
    ├── go/               # go test/build/vet, golangci-lint
    ├── js/               # npm, pnpm, npx, vitest, jest, tsc, eslint, prettier, next, prisma, playwright
    ├── python/           # ruff, pytest, mypy, pip
    ├── ruby/             # rake, rails test, rspec, rubocop
    ├── dotnet/           # dotnet CLI, binlog, trx, format reports
    ├── jvm/              # JVM-based tools
    └── cloud/            # aws, docker, kubectl, curl, wget, psql
```

Each `cmds/*` subdirectory ships its own README documenting file descriptions, parsing strategy, and
cross-command dependencies — a clean, contributor-friendly convention.

---

## 5. Supported Command Coverage

100+ commands across these categories:

- **File ops:** `ls`, `cat`/`read`, `grep`, `find`, `diff`, `tree`, `wc`
- **Git workflows:** `status`, `log`, `diff`, `add`, `commit`, `push` (e.g. push returns a terse `ok main`)
- **Test runners:** `jest`, `vitest`, `pytest`, `cargo test`, `go test`, `rspec` (typically **failures only**)
- **Build/lint:** `tsc`, `eslint`, `cargo clippy`, `ruff`, `mypy`, `rubocop`, `golangci-lint`
- **Package managers:** `npm`, `pnpm`, `pip`, `bundle`, `dotnet`
- **Cloud/containers:** AWS CLI, Docker, Kubernetes (`kubectl`)
- **VCS hosting CLIs:** GitHub CLI (`gh`), Graphite (`gt`)

---

## 6. Token-Savings Benchmarks

Reported figures (project's own measurements; treat as vendor claims):

| Source / scope                                    | Reduction        |
|---------------------------------------------------|------------------|
| Overall, 30-min Claude Code session (~118k→~23.9k)| **~80%**         |
| Average noise removed across 2,900+ real commands | **~89%**         |
| `cargo test`                                      | **~91.8%**       |
| Test runners (general)                            | ~90%             |
| `git add` / `commit` / `push`                     | up to **~92%**   |
| `git status`                                      | **~80.8%**       |
| `find`                                            | **~78.3%**       |
| `grep`                                            | **~49.5%**       |

Stated performance targets: **<10 ms** startup overhead, **<5 MB** memory, **60–90%** savings.

---

## 7. Installation & Usage

**Install** (multiple paths):
```
brew install rtk                                   # Homebrew
cargo install --git https://github.com/rtk-ai/rtk  # Cargo
curl ... | sh                                      # quick install script (Linux/macOS)
# or download a prebuilt binary (macOS / Linux / Windows) from GitHub Releases
```

**Set up the transparent hook:**
```
rtk init -g                 # Claude Code / Copilot by default
rtk init -g --agent gemini  # or cursor, cline, windsurf, etc.
```

**Use directly (without hook):**
```
rtk git status
rtk read src/main.rs
rtk grep "TODO" src/
rtk cargo build
rtk pnpm list
```

**Analytics & discovery:**
```
rtk gain        # show token savings statistics
rtk discover    # identify additional optimization opportunities
```

**Configuration:** `~/.config/rtk/config.toml` (TOML). Supports command exclusion lists and tee mode
(save full unfiltered output on failures).

---

## 8. AI-Tool Integration Model

RTK supports 13+ agent platforms via three integration mechanisms:

1. **Hook-based** (Claude Code, GitHub Copilot): PreToolUse hook rewrites Bash commands transparently.
2. **Plugin-based** (OpenCode, etc.): a TS/Python plugin intercepts commands before execution.
3. **Instruction-based** (Windsurf, Cline): project-scoped rule files instruct the agent to prefer `rtk`.

Compatible with: Claude Code, Cursor, Gemini CLI, Aider, Copilot, and "any AI assistant that reads
terminal output."

---

## 9. Engineering Conventions (from CLAUDE.md)

- **Language:** Rust (~92% of the codebase).
- **No async** — single-threaded by design (keeps the binary small/fast).
- **`anyhow::Result` + `.context()`** for error propagation.
- **Strict no-`unwrap()` policy** in production code.
- **`lazy_static!`** for all regex patterns.
- **Zero clippy warnings** required before commit.
- **Quality gate:** `cargo fmt --all && cargo clippy --all-targets && cargo test --all`.
- Smoke tests via `bash scripts/test-all.sh`.

This is a disciplined, performance-first codebase — fitting for a tool whose entire value proposition
is being a near-zero-cost interposer.

---

## 10. Project Status & Governance

- **Popularity:** ~52.8k GitHub stars, ~3.2k forks, 175+ releases (high-momentum project).
- **Core team:** Patrick Szymkowiak (founder), Florian Bruniaux, Adrien Eppling.
- **Community:** Discord + open GitHub contributions.

> **Source conflict — license & telemetry:** The repository's own docs (README/CLAUDE.md as fetched)
> state **Apache License 2.0** with **opt-in, anonymous, aggregate telemetry** (no source code, paths,
> secrets, or PII; `rtk telemetry status` / `forget` to manage). A third-party blog instead claims
> **MIT license, no telemetry**. **Trust the repository's `LICENSE` file and telemetry docs as
> authoritative** — verify directly before relying on either claim.

---

## 11. Critical Assessment

**Strengths**
- Attacks a real, growing cost center (agent token spend) with a simple, deterministic approach.
- Zero-config "transparent hook" is the right UX — no model retraining or prompt changes needed.
- Safe-by-design: fallback to raw output + tee-on-failure means it shouldn't break workflows.
- Per-command tuning is more reliable than a generic text summarizer (no hallucination risk; it's
  deterministic filtering, not an LLM compressing an LLM's input).

**Limitations / risks to weigh**
- **Lossy by definition.** Filters decide what's "noise"; an aggressive filter can drop a line the
  agent actually needed (e.g. a warning that explains a later failure). The fallback only triggers on
  *command* failure, not on *information* loss.
- **Built-in tool bypass.** In Claude Code, Read/Grep/Glob skip the hook, so savings depend on the
  agent choosing the shell path.
- **Vendor-reported benchmarks.** The 60–90% figures are the project's own; real savings depend
  heavily on workload mix (a session dominated by file reads vs. test runs behaves very differently).
- **Maintenance surface.** 100+ commands × many output formats = ongoing parser upkeep as tools change
  their output across versions.

**Verdict.** RTK is a well-engineered, pragmatic answer to agent token bloat. For teams running heavy
agentic coding sessions (especially test/build/git-loop heavy workflows), the cost and
context-window savings are plausibly significant. The right way to adopt it is to **measure your own
`rtk gain`** rather than assume the headline percentages, and to keep tee-on-failure enabled so full
logs remain available when debugging.

---

## 12. Relevance to "Token-Saving" as a Discipline

RTK exemplifies a broader pattern worth tracking: **deterministic, tool-aware output compression at
the I/O boundary**, as opposed to LLM-based summarization. Key transferable ideas:

- Compress at the **source of verbosity** (the command), not after it's already in context.
- Prefer **deterministic filters** over model-based summarization for tool output — cheaper, faster,
  and no hallucination of error messages.
- Always keep a **lossless escape hatch** (raw fallback / tee) so compression never blocks debugging.
- **Measure realized savings** per-workload rather than trusting global averages.

---

## Sources

- [rtk-ai/rtk — GitHub](https://github.com/rtk-ai/rtk)
- [RTK — Rust Token Killer (project site)](https://www.rtk-ai.app/)
- [rtk/CLAUDE.md at master](https://github.com/rtk-ai/rtk/blob/master/CLAUDE.md)
- [rtk/INSTALL.md at master](https://github.com/rtk-ai/rtk/blob/master/INSTALL.md)
- [rtk/CONTRIBUTING.md at master](https://github.com/rtk-ai/rtk/blob/master/CONTRIBUTING.md)
- [I Tried RTK (Rust Token Killer) — jangwook.net](https://jangwook.net/en/blog/en/rtk-rust-token-killer-llm-cost-optimization-guide-2026/)
