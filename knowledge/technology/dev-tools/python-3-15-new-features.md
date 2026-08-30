# Python 3.15 幾個值得關注的新特性:frozendict、Sentinel、lazy import

> 整理自 YouTube「程序员老王」〈Python 3.15 有什么新特性〉(約 6 分鐘)。Python 3.15 已釋出 Beta,距正式版一步之遙。本筆記挑出三個最有感的特性(**frozendict 不可變字典、`Sentinel` 哨兵物件、`lazy import` 惰性匯入**),外加幾個小而方便的改進,各配「以前怎麼解 / 現在怎麼解」的對照範例。

---

## 一句話總結

這三個特性共同點都是「**把以前要靠奇技淫巧繞的場景,變成語言內建的乾淨寫法**」:frozendict 讓「不可變映射」變一等公民、Sentinel 讓「沒傳值」的預設值不再污染型別標註、lazy import 讓「啟動慢但不一定用到的匯入」延後到真正用到時。

---

## ① frozendict:不可變字典(終於內建)

用法極簡:`frozendict(原字典)`,或用另一個字典初始化。兩大用途:

**用途一:需要回傳「不可變的預設值」,避免被呼叫者改到全域。**

```python
# ❌ 以前的雷:直接回傳全域 default,呼叫者一改就污染所有人拿到的預設值
_default = {"retries": 3}
def get_default():
    return _default        # 呼叫者 get_default()["retries"]=99 → 全域被改

# 舊解法:每次複製一份再回傳 → 代價是多一次 copy,CPU/記憶體都增加
def get_default():
    return dict(_default)

# ✅ 3.15:把 default 直接做成 frozendict,資料不可變,直接回傳也安全
_default = frozendict({"retries": 3})
def get_default():
    return _default        # 不可變,呼叫者改不動
```

**用途二:可當作 dict / set 的 key(普通 dict 不行)。**

```python
# ❌ 普通可變 dict 算不出穩定 hash,Python 不准它當 key
def get_cache(kwargs):       # kwargs 是 dict
    return _cache[kwargs]    # TypeError: unhashable type: 'dict'

# 舊解法:自己封裝一個類別、或把 dict 轉成 tuple…都很繞
# ✅ 3.15:frozendict 值不可變、hash 固定,直接能當 key
def get_cache(kwargs):
    return _cache[frozendict(kwargs)]
```

---

## ② Sentinel:乾淨的「哨兵物件」表達「沒傳值」

問題情境:一個函式想區分「使用者主動傳了 `None`/`NaN`」與「什麼都沒傳(用預設值)」。

```python
# ❌ 問題:用 None 當預設值時,無法分辨「使用者就是想傳 None」還是「沒傳」
def print_bool(x=None):
    if x is None:
        print("錯誤:沒有傳值")   # 使用者其實想問「None 是 True 還 False」也會誤觸這條
    else:
        print(bool(x))
```

**舊解法**:生成一個「私有 sentinel 物件」當預設值,因為它是模組私有、外部存取不到,函式一看到它就知道「使用者沒傳值」。但缺點是**不規範**,而且**一旦加型別標註就破功**:

```python
_MISSING = object()                 # 私有哨兵
def print_bool(x=_MISSING): ...
# 想標註只收 int 與 None 時,卻因為預設值是 object 的實例,
# 被迫把標註放寬成 object → 等於「什麼都能傳」,違背本意
def print_bool(x: int | None | object = _MISSING): ...   # ❌ 型別失去意義
```

**3.15 的 `Sentinel`**:把 `_MISSING` 從 `object()` 換成 `Sentinel`,參數中的字串只與除錯有關(慣例上寫成跟變數名一致),型別標註就能直接用這個 sentinel,**不會擴大 value 的取值範圍,型別也更清晰**。

```python
from typing import Sentinel        # (示意)
_MISSING = Sentinel("_MISSING")
def print_bool(x: int | None = _MISSING):
    if x is _MISSING:
        print("錯誤:沒有傳值")
    else:
        print(bool(x))
```

---

## ③ lazy import:惰性匯入(啟動加速)

問題:`import` 一執行,Python 立刻把整個模組(及它連帶 import 的一堆檔案)全讀進來,**程式一啟動就特別慢**——但被 import 的庫不一定會用到。

```python
# ❌ 模組頂層 import tqdm:只要有人 import 你的模組就會連帶載入 tqdm,
#    即使他只想用 other_function()(根本沒碰到進度條),純浪費時間與記憶體
import tqdm
def download(): ...      # 唯一用到 tqdm 的函式
def other_function(): ...

# ✅ 3.15:lazy import → 執行到這行不真的載入,只先綁一個代理物件,
#    直到 tqdm 真正被用到時才觸發真正的 import
lazy import tqdm
```

也可在命令列加 **`-X lazy_import=on`** 讓**所有普通 `import` 全變惰性載入**,不必改程式碼。作者評價:能實打實帶來啟動效能提升、相容性問題也不大,**未來有可能變成預設開啟**。

---

## ④ 其他小而方便的改進

- **推導式中可用 `*` 解包**:在 list/set/dict 推導式建容器時,終於能用星號展開,不論元素是 list、set 還是 dict。
- **`open()` 預設編碼改為 UTF-8**:以前不帶 `encoding` 參數會用「系統預設編碼」,不同系統/設定可能不一樣、編碼不對就讀成亂碼;3.15 統一用最流行的 **UTF-8**(對跨平台讀檔是一大解脫)。
- **新的取樣式效能分析器(sampling profiler)**:開銷極低,還能**直接掛到正在執行中的行程**上(影片稱之為值得單獨介紹的功能)。

---

## 應用案例 / 什麼時候用得上

- **寫函式庫回傳「常數設定」**:用 `frozendict` 回傳預設 config,徹底杜絕「使用者改到回傳值污染全域」的經典 bug,還省掉防禦性 `dict()` 複製的開銷。
- **做 cache / memoize 的 key**:參數含 dict 時,用 `frozendict(kwargs)` 直接當 cache key,不用再自己 hash 或轉 tuple。
- **設計「可選參數」API**:凡是「`None` 本身也是合法輸入值」的函式,用 `Sentinel` 當「沒傳」的哨兵,型別標註保持精確(只列真正合法型別),別再用 `object()` 把標註放寬到無意義。
- **加速 CLI / 大型套件啟動**:把重、又不一定用到的依賴(如 `tqdm`、`pandas`、`torch`)改成 `lazy import`,或直接跑 `-X lazy_import=on`,讓「只想用某個輕量函式」的使用者不必付整包載入的代價。
- **跨平台讀寫檔**:升上 3.15 後可少寫 `encoding='utf-8'`(預設已是它),減少 Windows/Linux 之間的亂碼坑。

> 相關:語言演進的取捨思路可對照 [[cpp-evolution-complexity-ai-era]](C++ 如何在加特性與控複雜度間拉扯)、[[dominating-programming-concepts]](當前主導的程式設計概念)。

---

## 來源

- 程序员老王,〈Python 3.15 有什么新特性〉,YouTube:<https://www.youtube.com/watch?v=t4QF0t_Y2Bs>(2026-06-11)
- 該片無字幕,逐字稿以 CPU 版 whisper.cpp(`pywhispercpp`,small 模型)轉錄取得,非官方字幕(可能有少量聽寫誤差,程式碼為依語意還原的示意寫法,實際 API 名稱以 Python 3.15 官方文件為準)。
