"""Tests for build_index.py: the --check integrity gate and index building.

Fixtures are tiny on-disk libraries built in a temp dir, so these run fast with
no PDFs and stdlib only: python -m unittest discover -s tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build_index  # noqa: E402


def make_book(root, slug, chapters, files_on_disk=None):
    """Write a book dir: manifest.json plus its chapter files.

    chapters: list of (file, title). files_on_disk overrides which files are
    actually created (default: every manifest file), to simulate drift.
    """
    book = root / slug
    book.mkdir(parents=True)
    manifest = {"title": slug.replace("-", " ").title(),
                "chapters": [{"file": f, "title": t} for f, t in chapters]}
    (book / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    for f in (files_on_disk if files_on_disk is not None else [f for f, _ in chapters]):
        (book / f).write_text("# stub\n", encoding="utf-8")
    return book


class FindProblemsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.lib = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_clean_library_has_no_problems(self):
        make_book(self.lib, "clean-book", [
            ("00-front-matter.md", "Front Matter"),
            ("ch01-intro.md", "Chapter 1. Intro"),
            ("ch02-more.md", "Chapter 2. More"),
            ("apA-notes.md", "Appendix A. Notes"),
        ])
        self.assertEqual(build_index.find_problems(self.lib), [])

    def test_missing_file_is_flagged(self):
        make_book(self.lib, "b", [("ch01-intro.md", "Chapter 1. Intro")], files_on_disk=[])
        self.assertTrue(any("missing on disk" in msg
                            for _, msg in build_index.find_problems(self.lib)))

    def test_orphan_file_is_flagged(self):
        book = make_book(self.lib, "b", [("ch01-intro.md", "Chapter 1. Intro")])
        (book / "ch99-stray.md").write_text("# stray\n", encoding="utf-8")
        self.assertTrue(any("orphan" in msg
                            for _, msg in build_index.find_problems(self.lib)))

    def test_duplicate_manifest_entry_is_flagged(self):
        make_book(self.lib, "b", [
            ("ch01-intro.md", "Chapter 1. Intro"),
            ("ch01-intro.md", "Chapter 1. Intro"),
        ])
        self.assertTrue(any("listed 2 times" in msg
                            for _, msg in build_index.find_problems(self.lib)))

    def test_duplicate_chapter_identity_is_flagged(self):
        # two different files both claiming chapter 4: the fundamentals echo bug
        make_book(self.lib, "b", [
            ("ch04-architectural.md", "Chapter 4. Architectural Characteristics Defined"),
            ("ch04-architecture.md", "Chapter 4: Architecture Characteristics Defined"),
        ])
        self.assertTrue(any("chapter 4" in msg
                            for _, msg in build_index.find_problems(self.lib)))


class ChapterKeyTests(unittest.TestCase):
    def test_parses_chapter_and_appendix(self):
        self.assertEqual(build_index.chapter_key("Chapter 6. Measuring"), ("chapter", "6"))
        self.assertEqual(build_index.chapter_key("Appendix B. Stats"), ("appendix", "b"))

    def test_unnumbered_titles_have_no_key(self):
        self.assertIsNone(build_index.chapter_key("Front Matter"))
        self.assertIsNone(build_index.chapter_key("Index"))


class BuildIndexTextTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.lib = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_counts_and_skips_front_matter(self):
        make_book(self.lib, "b", [
            ("00-front-matter.md", "Front Matter"),
            ("ch01-intro.md", "Chapter 1. Intro"),
        ])
        text, books, chapters = build_index.build_index_text(self.lib)
        self.assertEqual((books, chapters), (1, 1))    # front matter not counted
        self.assertIn("ch01-intro.md", text)
        self.assertNotIn("00-front-matter.md", text)   # 00- entries skipped from the index


if __name__ == "__main__":
    unittest.main()
