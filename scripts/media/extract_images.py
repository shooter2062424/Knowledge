"""從 PDF 或圖片素材產生「可放進 Markdown 筆記」的壓縮圖片。

素材(`new/` 收件匣)本身不進版控,但筆記裡的關鍵圖片一定要附上。
本腳本把 PDF 頁面或內嵌圖轉成縮小、壓縮過的 JPEG/PNG,輸出到筆記旁的
``assets/<筆記 slug>/`` 資料夾,並印出可直接貼進筆記的 Markdown 片段。

用法範例::

    # 列出 PDF 每頁有幾張內嵌圖、文字量,先決定哪些頁值得放
    python scripts/media/extract_images.py scan "new/ai-guide/x.pdf"

    # 把指定頁整頁渲染成圖(適合圖表/架構圖/投影片式頁面)
    python scripts/media/extract_images.py pages "new/ai-guide/x.pdf" 3 7 \
        --out knowledge/technology/ai-agents/foundations/assets/my-note --prefix x

    # 取出指定頁的內嵌圖片(照片/截圖)
    python scripts/media/extract_images.py embedded "new/ai-guide/x.pdf" 3 \
        --out knowledge/technology/ai-agents/foundations/assets/my-note --prefix x

    # 壓縮一張既有圖片(png/jpg/webp)
    python scripts/media/extract_images.py shrink "new/foo/chart.png" \
        --out knowledge/technology/ai-agents/foundations/assets/my-note
"""

from __future__ import annotations

import argparse
import io
import os
import sys

MAX_WIDTH = 1100
MAX_BYTES = 220_000


def save_compressed(img, dest_base: str) -> str:
    """把 PIL 圖片縮小並壓到 ``MAX_BYTES`` 以下後存檔。

    Args:
        img: ``PIL.Image.Image`` 物件。
        dest_base: 不含副檔名的輸出路徑。

    Returns:
        實際寫出的檔案路徑(含副檔名)。有透明度存 PNG,否則存 JPEG。
    """
    from PIL import Image

    if img.width > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)), Image.LANCZOS)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    if has_alpha:
        dest = dest_base + ".png"
        img.save(dest, optimize=True)
        return dest
    img = img.convert("RGB")
    dest = dest_base + ".jpg"
    quality = 82
    while True:
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=quality, optimize=True)
        if buf.tell() <= MAX_BYTES or quality <= 45:
            break
        quality -= 8
    with open(dest, "wb") as fh:
        fh.write(buf.getvalue())
    return dest


def scan_pdf(path: str) -> list[str]:
    """逐頁統計 PDF 的文字量與內嵌圖數量,協助挑選要放進筆記的頁面。

    Args:
        path: PDF 路徑。

    Returns:
        每頁一行的摘要文字。
    """
    import fitz

    doc = fitz.open(path)
    rows = [f"{path}: {doc.page_count} 頁"]
    for i, page in enumerate(doc, 1):
        rows.append(f"p{i}: 文字 {len(page.get_text())} 字, 內嵌圖 {len(page.get_images())}, 向量圖形 {len(page.get_drawings())}")
    return rows


def render_pages(path: str, pages: list[int], out_dir: str, prefix: str, zoom: float = 1.6) -> list[str]:
    """把 PDF 指定頁(1 起算)渲染成壓縮圖。

    Args:
        path: PDF 路徑。
        pages: 頁碼清單(1 起算)。
        out_dir: 輸出資料夾,不存在會建立。
        prefix: 檔名前綴。
        zoom: 渲染縮放倍率。

    Returns:
        輸出檔路徑清單。
    """
    import fitz
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(path)
    out: list[str] = []
    for p in pages:
        pix = doc[p - 1].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        out.append(save_compressed(img, os.path.join(out_dir, f"{prefix}-p{p}")))
    return out


def extract_embedded(path: str, pages: list[int], out_dir: str, prefix: str, min_side: int = 250) -> list[str]:
    """取出 PDF 指定頁的內嵌圖片(略過過小或在 3 頁以上重複的頭像/logo/裝飾圖)。

    Args:
        path: PDF 路徑。
        pages: 頁碼清單(1 起算)。
        out_dir: 輸出資料夾。
        prefix: 檔名前綴。
        min_side: 寬或高小於此值的圖視為圖示而略過。

    Returns:
        輸出檔路徑清單。
    """
    import fitz
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(path)
    count: dict[int, int] = {}
    for page in doc:
        for info in page.get_images(full=True):
            count[info[0]] = count.get(info[0], 0) + 1
    out: list[str] = []
    for p in pages:
        for n, info in enumerate(doc[p - 1].get_images(full=True), 1):
            pix = fitz.Pixmap(doc, info[0])
            if pix.width < min_side or pix.height < min_side or count[info[0]] > 2:
                continue  # 太小或重複出現(頭像/logo/裝飾)
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
            out.append(save_compressed(img, os.path.join(out_dir, f"{prefix}-p{p}-{n}")))
    return out


def dump_text(path: str) -> list[str]:
    """取出 PDF 的可複製文字,每頁以分隔線標示頁碼。

    Args:
        path: PDF 路徑。

    Returns:
        文字行清單(沒有文字層的頁面會標註「無文字層」)。
    """
    import fitz

    out: list[str] = []
    for i, page in enumerate(fitz.open(path), 1):
        t = page.get_text().strip()
        out.append(f"===== p{i} =====")
        out.append(t if t else "(無文字層:需看圖轉寫)")
    return out


def list_figures(path: str) -> list[str]:
    """列出 PDF 的內嵌圖,標記疑似頭像/logo/裝飾圖(重複出現或小的正方形)。

    Args:
        path: PDF 路徑。

    Returns:
        每張圖一行:頁碼、xref、尺寸、重複頁數與判斷。
    """
    import fitz

    doc = fitz.open(path)
    pages_of: dict[int, list[int]] = {}
    for i, page in enumerate(doc, 1):
        for info in page.get_images(full=True):
            pages_of.setdefault(info[0], []).append(i)
    rows = []
    for xref, pgs in pages_of.items():
        meta = doc.extract_image(xref)
        w, h = meta["width"], meta["height"]
        square = abs(w - h) <= 0.05 * max(w, h)
        skip = len(pgs) > 2 or (square and max(w, h) <= 800) or min(w, h) < 200
        rows.append(f"p{pgs[0]} xref={xref} {w}x{h} 出現{len(pgs)}頁 {'略過(疑似頭像/logo/裝飾)' if skip else '候選圖表'}")
    return rows


def crop_region(path: str, page: int, box: tuple[float, float, float, float], out_dir: str, prefix: str, zoom: float = 2.0) -> str:
    """從 PDF 頁面裁出一個區塊(以頁面寬高比例指定)並壓縮輸出。

    Args:
        path: PDF 路徑。
        page: 頁碼(1 起算)。
        box: ``(x0, y0, x1, y1)``,皆為 0–1 的頁面寬高比例。
        out_dir: 輸出資料夾。
        prefix: 檔名前綴。
        zoom: 渲染倍率。

    Returns:
        輸出檔路徑。
    """
    import fitz
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    pg = fitz.open(path)[page - 1]
    r = pg.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height, r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    tag = "-".join(f"{int(v * 100)}" for v in box)
    return save_compressed(img, os.path.join(out_dir, f"{prefix}-p{page}-crop{tag}"))


def shrink_image(path: str, out_dir: str) -> str:
    """壓縮一張既有圖片。

    Args:
        path: 圖片路徑。
        out_dir: 輸出資料夾。

    Returns:
        輸出檔路徑。
    """
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    return save_compressed(Image.open(path), os.path.join(out_dir, stem))


def main() -> None:
    """命令列進入點。"""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("scan", "text", "figures"):
        p = sub.add_parser(name)
        p.add_argument("pdf")
    p = sub.add_parser("crop")
    p.add_argument("pdf")
    p.add_argument("page", type=int)
    p.add_argument("box", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--out", required=True)
    p.add_argument("--prefix", required=True)
    for name in ("pages", "embedded"):
        p = sub.add_parser(name)
        p.add_argument("pdf")
        p.add_argument("pages", type=int, nargs="+")
        p.add_argument("--out", required=True)
        p.add_argument("--prefix", required=True)
    p = sub.add_parser("shrink")
    p.add_argument("image")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "scan":
        files = scan_pdf(a.pdf)
    elif a.cmd == "text":
        files = dump_text(a.pdf)
    elif a.cmd == "figures":
        files = list_figures(a.pdf)
    elif a.cmd == "crop":
        files = [crop_region(a.pdf, a.page, tuple(a.box), a.out, a.prefix)]
    elif a.cmd == "pages":
        files = render_pages(a.pdf, a.pages, a.out, a.prefix)
    elif a.cmd == "embedded":
        files = extract_embedded(a.pdf, a.pages, a.out, a.prefix)
    else:
        files = [shrink_image(a.image, a.out)]
    for f in files:
        print(f)
        if a.cmd in ("pages", "embedded", "crop", "shrink"):
            slug = os.path.basename(os.path.dirname(f))
            print(f"  Markdown(筆記與 assets/ 同層時): ![說明](assets/{slug}/{os.path.basename(f)})")


if __name__ == "__main__":
    main()
