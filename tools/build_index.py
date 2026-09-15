#!/usr/bin/env python3
"""build_index.py - Assemble library/INDEX.md from every book's manifest.json.

The index is the retrieval entry point for agents: one line per chapter with
topic keywords and the file path. Agents grep this file first, then open only
the matching chapter file(s).

Usage:
  python3 build_index.py --library library           # build and write INDEX.md
  python3 build_index.py --library library --check    # validate only; write nothing

--check exits non-zero when a book has manifest/disk drift or duplicate
chapters, the failure modes that produce a broken or doubled index. Use it as a
gate after converting a book or in CI.
"""

import argparse
import json
import re
import sys
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "by", "for", "from", "how", "in", "into",
    "is", "it", "of", "on", "or", "the", "to", "using", "with", "your", "chapter",
    "appendix", "part", "hands", "hands-on", "why", "what",
}


def keywords(title: str) -> str:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#-]*", title.lower())
    kept = [w for w in words if w not in STOPWORDS and len(w) > 2]
    seen, out = set(), []
    for w in kept:
        if w not in seen:
            seen.add(w)
            out.append(w)
    return ", ".join(out)


CHAPTER_KEY_RE = re.compile(r"^(chapter|appendix)\s+([0-9]+|[a-z])\b", re.IGNORECASE)


def chapter_key(title: str):
    """Chapter or appendix identity from a title, e.g. ('chapter', '6').

    Returns None for anything that is not a numbered chapter or lettered
    appendix (front matter, an index, a preface), so those never collide.
    """
    m = CHAPTER_KEY_RE.match(title.strip())
    return (m.group(1).lower(), m.group(2).lower()) if m else None


def find_problems(library: Path):
    """Return a list of (slug, message) integrity problems across the library.

    Catches the states that yield a broken or duplicated index:
      - a manifest entry whose file is missing on disk (a dead index link),
      - an orphan .md on disk that no manifest entry references (stale drift),
      - the same file listed more than once in one manifest,
      - two chapters that resolve to the same chapter or appendix number.
    """
    problems = []
    for mpath in sorted(library.glob("*/manifest.json")):
        book = mpath.parent
        slug = book.name
        try:
            manifest = json.loads(mpath.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            problems.append((slug, f"unreadable manifest.json: {exc}"))
            continue

        chapters = manifest.get("chapters", [])
        files = [ch.get("file", "") for ch in chapters]

        for f in files:
            if not f:
                problems.append((slug, "a chapter entry has no 'file'"))
            elif not (book / f).is_file():
                problems.append((slug, f"manifest lists {f!r}, missing on disk"))

        listed = set(files)
        for p in sorted(book.glob("*.md")):
            if p.name not in listed:
                problems.append((slug, f"orphan file {p.name!r} not in manifest"))

        for f in sorted(set(files)):
            n = files.count(f)
            if f and n > 1:
                problems.append((slug, f"file {f!r} listed {n} times in manifest"))

        by_key = {}
        for ch in chapters:
            key = chapter_key(ch.get("title", ""))
            if key:
                by_key.setdefault(key, []).append(ch.get("file", ""))
        for key, fs in sorted(by_key.items()):
            if len(fs) > 1:
                problems.append((slug, f"{key[0]} {key[1]} claimed by {len(fs)} files: {sorted(fs)}"))

    return problems


def build_index_text(library: Path):
    """Build the index text. Returns (text, book_count, chapter_entry_count)."""
    manifests = sorted(library.glob("*/manifest.json"))
    if not manifests:
        raise SystemExit(f"No manifest.json files under {library}/ - run convert_book.py first.")

    lines = [
        "# Library Index",
        "",
        "Full-text reference library (gitignored, personal copies). Retrieval protocol for agents:",
        "1. Grep this file for topic keywords to find the relevant chapter(s).",
        "2. Read ONLY the matching chapter file(s), never a whole book.",
        "3. If a lookup answered a real project question, propose promoting the answer",
        "   into docs/standards/ with a citation (book, chapter).",
        "",
    ]

    total = 0
    for mpath in manifests:
        m = json.loads(mpath.read_text(encoding="utf-8"))
        slug = mpath.parent.name
        lines.append(f"## {m['title']}  (`{library.name}/{slug}/`)")
        lines.append("")
        for ch in m["chapters"]:
            if ch["file"].startswith("00-"):
                continue  # front matter adds noise, skip from the index
            kw = keywords(ch["title"])
            lines.append(f"- `{slug}/{ch['file']}` - {ch['title']}" + (f"  [{kw}]" if kw else ""))
            total += 1
        lines.append("")

    return "\n".join(lines) + "\n", len(manifests), total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--library", type=Path, default=Path("library"))
    ap.add_argument("--check", action="store_true",
                    help="Validate for manifest/disk drift and duplicate chapters; write nothing, exit non-zero on problems")
    args = ap.parse_args()

    if args.check:
        problems = find_problems(args.library)
        for slug, msg in problems:
            print(f"[BAD] {slug}: {msg}", file=sys.stderr)
        if problems:
            print(f"\n{len(problems)} integrity problem(s) in {args.library}/.", file=sys.stderr)
            return 1
        print(f"Library OK: no drift or duplicate chapters in {args.library}/.")
        return 0

    text, books, chapters = build_index_text(args.library)
    out = args.library / "INDEX.md"
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out} ({books} book(s), {chapters} chapter entries)")

    problems = find_problems(args.library)
    if problems:
        print(f"warning: {len(problems)} integrity problem(s); run: build_index.py --check",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
