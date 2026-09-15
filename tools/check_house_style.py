#!/usr/bin/env python3
"""check_house_style.py - Enforce the two house writing rules on authored files.

Rules (docs/standards/writing-style.md):
  1. No AI attribution signatures: co-author trailers, "generated with" notices,
     an Anthropic noreply address, or the robot emoji.
  2. No em-dash character (U+2014).

The reference library under library/ is third-party text and is exempt. The rule
text in the standards describes the ban without using the actual signatures, so
this checker matches signatures, not prose, and does not flag the standards.

Modes:
  --staged      Check the STAGED content of files staged for commit (git diff
                --cached, read via git show). Used by the pre-commit hook; exits
                non-zero to block the commit on a violation.
  --hook        Read a Claude Code PostToolUse event on stdin and check the one file
                it wrote or edited. Advisory: prints to stderr and exits 2 on a
                violation, 0 otherwise, and never fails the session on an error.
  <paths...>    Check the given files on disk.

Exit codes: 0 clean; 1 violations found (staged or explicit modes); 2 violation
found (--hook). Any internal error in --hook mode exits 0 so a session is never
broken by this check.
"""
import sys
import os
import json
import re
import subprocess

EMDASH = chr(0x2014)
ROBOT = chr(0x1F916)

# Attribution SIGNATURES, not prose about attribution.
ATTRIB_PATTERNS = [
    re.compile(r"^\s*Co-Authored-By:\s", re.IGNORECASE | re.MULTILINE),
    re.compile(r"Generated with \[?Claude", re.IGNORECASE),
    re.compile(r"noreply@anthropic\.com", re.IGNORECASE),
    re.compile(re.escape(ROBOT)),
]

TEXT_EXTS = {".md", ".py", ".txt", ".json", ".yml", ".yaml", ".toml", ".cfg",
             ".ini", ".sh", ".js", ".ts", ".tsx", ".jsx", ".css", ".html"}
NAMED_TEXT = {".editorconfig", ".gitignore", ".gitattributes"}


def is_exempt(path):
    p = path.replace("\\", "/")
    return (p.startswith("library/") or "/library/" in p
            or p.startswith(".git/") or "/.git/" in p)


def looks_text(path):
    base = os.path.basename(path)
    if base in NAMED_TEXT:
        return True
    return os.path.splitext(path)[1].lower() in TEXT_EXTS


def scan_text(text):
    """Return a list of (line_no, rule, snippet) for the two house rules."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if EMDASH in line:
            out.append((i, "em-dash (U+2014)", line.strip()[:80]))
    for pat in ATTRIB_PATTERNS:
        for m in pat.finditer(text):
            ln = text.count("\n", 0, m.start()) + 1
            out.append((ln, "AI attribution", m.group(0).strip()[:80]))
    return out


def check_file(path):
    """Scan a file on disk. Exempt, non-text, missing, or binary -> []."""
    if is_exempt(path) or not looks_text(path) or not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            return scan_text(fh.read())
    except (OSError, UnicodeDecodeError):
        return []


def staged_paths():
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return []
    return [ln for ln in res.stdout.splitlines() if ln.strip()]


def check_staged(path):
    """Scan the STAGED blob of a path (what the commit will contain), not disk."""
    if is_exempt(path) or not looks_text(path):
        return []
    try:
        res = subprocess.run(["git", "show", f":{path}"],
                             capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return []
    try:
        return scan_text(res.stdout.decode("utf-8"))
    except UnicodeDecodeError:
        return []


def report(paths, checker):
    total = 0
    for path in paths:
        for ln, rule, snip in checker(path):
            print(f"{path}:{ln}: {rule}: {snip}", file=sys.stderr)
            total += 1
    return total


def run_hook():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    if not isinstance(event, dict):
        return 0
    ti = event.get("tool_input")
    path = ti.get("file_path") if isinstance(ti, dict) else None
    if not isinstance(path, str) or not path:
        return 0
    cwd = event.get("cwd")
    rel = path
    if isinstance(cwd, str):
        try:
            rel = os.path.relpath(path, cwd)
        except ValueError:
            rel = path
    if is_exempt(rel):
        return 0
    try:
        viols = check_file(path)
    except OSError:
        return 0
    if not viols:
        return 0
    print(f"House style: {len(viols)} issue(s) in {rel} "
          f"(docs/standards/writing-style.md). Fix before committing:",
          file=sys.stderr)
    for ln, rule, snip in viols:
        print(f"  line {ln}: {rule}: {snip}", file=sys.stderr)
    return 2


def main():
    args = sys.argv[1:]
    if "--hook" in args:
        try:
            return run_hook()
        except Exception:  # advisory hook must never break a session
            return 0
    if "--staged" in args:
        n = report(staged_paths(), check_staged)
        if n:
            print(f"\n{n} house-style violation(s) in staged content. Commit blocked "
                  f"(docs/standards/writing-style.md).", file=sys.stderr)
            return 1
        return 0
    paths = [a for a in args if not a.startswith("--")]
    if not paths:
        print("usage: check_house_style.py [--staged | --hook | <files...>]",
              file=sys.stderr)
        return 0
    return 1 if report(paths, check_file) else 0


if __name__ == "__main__":
    sys.exit(main())
