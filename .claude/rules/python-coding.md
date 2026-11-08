---
paths:
  - "**/*.py"
---

# Python coding and commit rules (user, 2026-11-09)

Apply to new files and files you substantially rewrite. Before committing, scan for one-line docstrings and unaligned declaration blocks.

## 1. Docstrings, type hints, comments
- Every function gets an English Google-style docstring, private helpers included.
- The brief goes on the line AFTER the opening `"""`. Never use a one-line `"""Text."""`.
- Then an optional detail paragraph, `Args:`, `Returns:`, and `Raises:` (add it when the function raises on purpose).
- Write `None.` under `Args:` when the function has no arguments.
- PEP 484 type hints on every signature, using built-in generics (`list[int]`, `X | None`) and `from __future__ import annotations`.
- Comments explain the WHY and stay short.

## 2. Alignment
- In blocks of consecutive declarations (module constants, Enum members, `@dataclass` fields), align the `:` of type hints into one column and the `=` into one column. Keep at least one space on each side of `=`.
- Keyword arguments and defaults inside a call or signature stay PEP 8: `f(x=1)`.
- Align trailing `#` comments within the block too.

```python
SPAN_DAYS  = 156 * 7      # look back at most 156 weeks
BASE_TOL   = 0.05

@dataclass
class Level:
    side:  str
    price: float
    prob:  int | None = None
```

## 3. Commits
- Subject format is `[type] msg`; type is one of `feat`, `fix`, `docs`, `refactor`, `chore`, `build`, `release`.
- No attribution trailers: no `Co-Authored-By`, no `Claude-Session`.

## Note
This supersedes the older `CLAUDE.md` wording that allowed Chinese briefs in `scripts/` docstrings, and the earlier trailer convention.
