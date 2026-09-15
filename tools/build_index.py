#!/usr/bin/env python3
"""build_index.py - Assemble library/INDEX.md from every book's manifest.json.

The index is the retrieval entry point for agents: one line per chapter with
topic keywords and the file path. Agents grep this file first, then open only
the matching chapter file(s).

Usage:
  python3 build_index.py --library library
"""

import argparse
import json
import re
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--library", type=Path, default=Path("library"))
    args = ap.parse_args()

    manifests = sorted(args.library.glob("*/manifest.json"))
    if not manifests:
        raise SystemExit(f"No manifest.json files under {args.library}/ - run convert_book.py first.")

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
        lines.append(f"## {m['title']}  (`{args.library.name}/{slug}/`)")
        lines.append("")
        for ch in m["chapters"]:
            if ch["file"].startswith("00-"):
                continue  # front matter adds noise, skip from the index
            kw = keywords(ch["title"])
            lines.append(f"- `{slug}/{ch['file']}` - {ch['title']}" + (f"  [{kw}]" if kw else ""))
            total += 1
        lines.append("")

    out = args.library / "INDEX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(manifests)} book(s), {total} chapter entries)")


if __name__ == "__main__":
    main()
