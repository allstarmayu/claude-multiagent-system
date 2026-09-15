"""Tests for convert_book.py's chapter-detection helpers.

These are the guards against the corruption fixed in the fundamentals book: echo
bookmarks that duplicated every chapter, and titles with line breaks or
non-breaking spaces. The helpers are pure, but importing convert_book needs
pymupdf, so the suite skips cleanly when it is not installed.
Run: python -m unittest discover -s tests
"""
import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

try:
    convert_book = importlib.import_module("convert_book")
except Exception:  # pymupdf / pymupdf4llm not installed in this environment
    convert_book = None

NBSP = chr(0xA0)


@unittest.skipUnless(convert_book, "pymupdf not installed; skipping convert_book tests")
class NormspaceTests(unittest.TestCase):
    def test_collapses_line_break(self):
        self.assertEqual(
            convert_book.normspace("Chapter 6. Measuring and Governing \nArchitecture"),
            "Chapter 6. Measuring and Governing Architecture")

    def test_collapses_non_breaking_space(self):
        self.assertEqual(convert_book.normspace(f"Chapter{NBSP}4: Title"), "Chapter 4: Title")

    def test_strips_ends(self):
        self.assertEqual(convert_book.normspace("  padded title  "), "padded title")


@unittest.skipUnless(convert_book, "pymupdf not installed; skipping convert_book tests")
class DedupeChapterIdentityTests(unittest.TestCase):
    def test_drops_echoes_keeping_first_occurrence(self):
        # real chapters at front pages, echo copies at back pages
        entries = [
            ("Chapter 1. Introduction", 25),
            ("Chapter 4. Architectural Characteristics Defined", 79),
            ("Chapter 1: Introduction", 521),                     # echo of ch 1
            ("Chapter 4: Architecture Characteristics Defined", 522),  # echo of ch 4
        ]
        self.assertEqual(convert_book.dedupe_chapter_identity(entries), [
            ("Chapter 1. Introduction", 25),
            ("Chapter 4. Architectural Characteristics Defined", 79),
        ])

    def test_keeps_distinct_chapters_and_appendices(self):
        entries = [("Chapter 1. A", 1), ("Chapter 2. B", 2),
                   ("Appendix A. X", 3), ("Appendix B. Y", 4)]
        self.assertEqual(convert_book.dedupe_chapter_identity(entries), entries)


@unittest.skipUnless(convert_book, "pymupdf not installed; skipping convert_book tests")
class ChapterFilenameTests(unittest.TestCase):
    def test_chapter_and_appendix_naming(self):
        self.assertEqual(convert_book.chapter_filename(3, "Chapter 6. Measuring"), "ch06-measuring.md")
        self.assertEqual(convert_book.chapter_filename(9, "Appendix B. The Stats"), "apB-the-stats.md")

    def test_normalized_multiline_title_names_cleanly(self):
        title = convert_book.normspace("Chapter 6. Measuring and Governing \nArchitecture Characteristics")
        self.assertEqual(convert_book.chapter_filename(5, title),
                         "ch06-measuring-and-governing-architecture-characteristics.md")


if __name__ == "__main__":
    unittest.main()
