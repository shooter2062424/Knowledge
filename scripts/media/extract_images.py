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


def extract_embedded(path: str, pages: list[int], out_dir: str, prefix: str, min_side: int = 160) -> list[str]:
    """取出 PDF 指定頁的內嵌圖片(略過過小的裝飾圖)。

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
    out: list[str] = []
    for p in pages:
        for n, info in enumerate(doc[p - 1].get_images(full=True), 1):
            pix = fitz.Pixmap(doc, info[0])
            if pix.width < min_side or pix.height < min_side:
                continue
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
            out.append(save_compressed(img, os.path.join(out_dir, f"{prefix}-p{p}-{n}")))
    return out


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
    p = sub.add_parser("scan")
    p.add_argument("pdf")
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
    elif a.cmd == "pages":
        files = render_pages(a.pdf, a.pages, a.out, a.prefix)
    elif a.cmd == "embedded":
        files = extract_embedded(a.pdf, a.pages, a.out, a.prefix)
    else:
        files = [shrink_image(a.image, a.out)]
    for f in files:
        print(f)
        if a.cmd != "scan":
            slug = os.path.basename(os.path.dirname(f))
            print(f"  Markdown(筆記與 assets/ 同層時): ![說明](assets/{slug}/{os.path.basename(f)})")


if __name__ == "__main__":
    main()
