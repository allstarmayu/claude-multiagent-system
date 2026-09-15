#!/usr/bin/env python3
"""convert_book.py - Convert book PDFs into per-chapter markdown for an agent reference library.

Pipeline per book:
  1. Triage: verify the PDF has a text layer (scanned books are flagged for OCR, not converted).
  2. Split: find chapter boundaries via embedded bookmarks; fall back to scanning
     pages for "Chapter N" headings when bookmarks are missing or useless.
  3. Extract: render each chapter to markdown with pymupdf4llm.
  4. Record: write manifest.json so build_index.py can assemble the library index.

Usage:
  python3 convert_book.py book1.pdf book2.pdf --out library
  python3 convert_book.py book.pdf --out library --slug release-it
  python3 convert_book.py scanned.pdf --out library --force   (convert despite low text yield)
"""

import argparse
import json
import re
import sys
import unicodedata
from glob import glob
from pathlib import Path

import pymupdf
import pymupdf4llm

CHAPTER_TOC_RE = re.compile(r"^(chapter|appendix)\b", re.IGNORECASE)
CHAPTER_HEAD_RE = re.compile(r"^\s*chapter\s+(\d{1,3})\b[.:\s-]*(.*)$", re.IGNORECASE | re.MULTILINE)


def slugify(text: str, maxlen: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:maxlen].rstrip("-") or "untitled"


def triage_chars_per_page(doc: pymupdf.Document, samples: int = 12) -> float:
    """Average extractable characters per page across a spread of sample pages."""
    n = doc.page_count
    if n == 0:
        return 0.0
    idxs = sorted({round(i * (n - 1) / max(samples - 1, 1)) for i in range(min(samples, n))})
    counts = [len(doc[i].get_text("text")) for i in idxs]
    return sum(counts) / len(counts)


def chapters_from_bookmarks(doc: pymupdf.Document):
    """Prefer bookmark entries that literally say Chapter/Appendix; else plausible level-1 set."""
    toc = doc.get_toc(simple=True)
    if not toc:
        return None
    hits = [(title.strip(), page) for _, title, page in toc if CHAPTER_TOC_RE.match(title.strip())]
    if len(hits) >= 4:
        return dedupe_increasing(hits)
    level1 = [(title.strip(), page) for lvl, title, page in toc if lvl == 1]
    if 5 <= len(level1) <= 60:
        return dedupe_increasing(level1)
    return None


def chapters_from_page_scan(doc: pymupdf.Document):
    """Fallback: pages whose text begins with a lone 'Chapter N' heading near the top.

    Pages containing many 'Chapter N' strings (printed tables of contents) are skipped.
    """
    found = {}
    for i in range(doc.page_count):
        text = doc[i].get_text("text")
        matches = list(CHAPTER_HEAD_RE.finditer(text))
        if len(matches) != 1 or matches[0].start() > 400:
            continue
        num = int(matches[0].group(1))
        title_rest = matches[0].group(2).strip()
        if not title_rest:  # title often sits on the next non-empty line
            after = text[matches[0].end():].strip().splitlines()
            title_rest = after[0].strip() if after else ""
        if num not in found:
            found[num] = (f"Chapter {num}: {title_rest}".rstrip(": "), i + 1)
    if len(found) < 3:
        return None
    ordered = [found[k] for k in sorted(found)]
    return dedupe_increasing(ordered)


def dedupe_increasing(entries):
    """Keep entries with strictly increasing page numbers (drops TOC echoes)."""
    out, last = [], 0
    for title, page in entries:
        if page > last:
            out.append((title, page))
            last = page
    return out


def chapter_filename(idx: int, title: str) -> str:
    m = re.match(r"^chapter\s+(\d{1,3})\b[.:\s-]*(.*)$", title, re.IGNORECASE)
    if m:
        return f"ch{int(m.group(1)):02d}-{slugify(m.group(2) or 'chapter')}.md"
    m = re.match(r"^appendix\s+([a-z0-9]{1,3})\b[.:\s-]*(.*)$", title, re.IGNORECASE)
    if m:
        return f"ap{m.group(1).upper()}-{slugify(m.group(2) or 'appendix')}.md"
    return f"{idx:02d}-{slugify(title)}.md"


def extract_markdown(doc: pymupdf.Document, pages_zero_based):
    """Version-tolerant pymupdf4llm call: newer kwargs first, plain call as fallback."""
    for kwargs in (
        {"pages": pages_zero_based, "show_progress": False, "ignore_images": True},
        {"pages": pages_zero_based, "show_progress": False},
        {"pages": pages_zero_based},
    ):
        try:
            return pymupdf4llm.to_markdown(doc, **kwargs)
        except TypeError:
            continue
    return pymupdf4llm.to_markdown(doc, pages=pages_zero_based)


def clean_markdown(md: str) -> str:
    md = re.sub(r"[ \t]+$", "", md, flags=re.MULTILINE)      # trailing whitespace
    md = re.sub(r"^\s*-----\s*$", "", md, flags=re.MULTILINE)  # page-break rules pymupdf4llm emits
    md = re.sub(r"\n{3,}", "\n\n", md)                        # collapse blank runs
    return md.strip() + "\n"


def convert(pdf_path: Path, out_root: Path, slug: str | None, min_chars: float, force: bool) -> bool:
    doc = pymupdf.open(pdf_path)
    title = (doc.metadata or {}).get("title") or pdf_path.stem
    book_slug = slug or slugify(title, maxlen=40)
    book_dir = out_root / book_slug

    avg_chars = triage_chars_per_page(doc)
    if avg_chars < min_chars and not force:
        print(f"[SKIP] {pdf_path.name}: ~{avg_chars:.0f} chars/page -> looks scanned or image-based.")
        print("       Run OCR first (e.g. `ocrmypdf in.pdf out.pdf`) or re-run with --force.")
        return False

    chapters = chapters_from_bookmarks(doc)
    method = "bookmarks"
    if not chapters:
        chapters = chapters_from_page_scan(doc)
        method = "page-scan"
    if not chapters:
        chapters = [(title, 1)]
        method = "whole-book (no chapter boundaries found - split manually if needed)"

    book_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"title": title, "source_pdf": pdf_path.name, "pages": doc.page_count,
                "split_method": method, "chapters": []}

    # Front matter: everything before the first detected chapter.
    first_page = chapters[0][1]
    if first_page > 1:
        chapters = [("Front Matter", 1)] + chapters

    for idx, (ch_title, start) in enumerate(chapters):
        end = (chapters[idx + 1][1] - 1) if idx + 1 < len(chapters) else doc.page_count
        if end < start:
            continue
        fname = "00-front-matter.md" if ch_title == "Front Matter" else chapter_filename(idx, ch_title)
        md = clean_markdown(extract_markdown(doc, list(range(start - 1, end))))
        header = f"<!-- {title} | {ch_title} | PDF pages {start}-{end} -->\n\n"
        (book_dir / fname).write_text(header + md, encoding="utf-8")
        manifest["chapters"].append({"file": fname, "title": ch_title, "pdf_pages": [start, end]})
        print(f"  {fname:<55} pp {start}-{end}")

    (book_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[OK] {title} -> {book_dir}  ({len(manifest['chapters'])} files, split via {method})")
    return True


def expand_inputs(items) -> list[Path]:
    """Turn folders and glob patterns into concrete PDF paths.

    PowerShell and cmd.exe pass wildcards like *.pdf to the script literally
    (no shell expansion), so we glob here. Folders expand to their *.pdf files.
    """
    out: list[Path] = []
    for item in items:
        p = Path(item)
        if p.is_dir():
            out.extend(sorted(p.glob("*.pdf")) + sorted(p.glob("*.PDF")))
        elif any(ch in str(item) for ch in "*?["):
            out.extend(Path(m) for m in sorted(glob(str(item))))
        else:
            out.append(p)
    seen, unique = set(), []
    for p in out:
        key = str(p.resolve()) if p.exists() else str(p)
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="+",
                    help="PDF files, glob patterns, or folders containing PDFs")
    ap.add_argument("--out", type=Path, default=Path("library"))
    ap.add_argument("--slug", help="Folder name for the book (single-PDF runs only)")
    ap.add_argument("--min-chars", type=float, default=200.0,
                    help="Triage threshold: avg extractable chars/page below this flags the book as scanned")
    ap.add_argument("--force", action="store_true", help="Convert even if triage flags the book as scanned")
    args = ap.parse_args()

    pdfs = expand_inputs(args.pdfs)
    if not pdfs:
        sys.exit(f"No PDFs matched: {' '.join(args.pdfs)}")
    if args.slug and len(pdfs) > 1:
        sys.exit("--slug only makes sense with a single PDF")

    ok = 0
    for pdf in pdfs:
        if not pdf.exists():
            print(f"[MISS] {pdf} not found")
            continue
        print(f"\n=== {pdf.name} ===")
        try:
            ok += convert(pdf, args.out, args.slug, args.min_chars, args.force)
        except Exception as exc:  # keep batch runs alive; report and continue
            print(f"[FAIL] {pdf.name}: {exc}")
    print(f"\nConverted {ok}/{len(pdfs)} book(s) into {args.out}/")


if __name__ == "__main__":
    main()
