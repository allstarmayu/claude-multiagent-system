"""Tests for check_house_style.py: the two house writing rules and exemptions.

The attribution signatures below are assembled from fragments at runtime, so the
literal signature never appears in this source file and the checker (and its
write-time hook) does not flag this test. Run: python -m unittest discover -s tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check_house_style as chs  # noqa: E402

EMDASH = chr(0x2014)
ROBOT = chr(0x1F916)
# Split so the verbatim signature is absent from this file but whole at runtime.
GENERATED = "Generated with " + "Claude Code"
NOREPLY = "noreply@" + "anthropic.com"
COAUTHOR = "Co-Authored" + "-By: A Name <x@y.z>"


class ScanTextTests(unittest.TestCase):
    def test_clean_text_passes(self):
        self.assertEqual(chs.scan_text("A clean line, with commas and (parentheses).\n"), [])

    def test_emdash_is_flagged(self):
        hits = chs.scan_text(f"A dash{EMDASH}in a sentence.\n")
        self.assertTrue(any("em-dash" in rule for _, rule, _ in hits))

    def test_coauthor_trailer_is_flagged(self):
        hits = chs.scan_text(COAUTHOR + "\n")
        self.assertTrue(any("attribution" in rule for _, rule, _ in hits))

    def test_generated_with_notice_is_flagged(self):
        hits = chs.scan_text("Footer: " + GENERATED + "\n")
        self.assertTrue(any("attribution" in rule for _, rule, _ in hits))

    def test_noreply_address_is_flagged(self):
        hits = chs.scan_text("contact " + NOREPLY + " here\n")
        self.assertTrue(any("attribution" in rule for _, rule, _ in hits))

    def test_robot_emoji_is_flagged(self):
        hits = chs.scan_text("shipped " + ROBOT + " today\n")
        self.assertTrue(any("attribution" in rule for _, rule, _ in hits))


class ExemptionTests(unittest.TestCase):
    def test_library_paths_are_exempt(self):
        self.assertTrue(chs.is_exempt("library/some-book/ch01.md"))
        self.assertTrue(chs.is_exempt("nested/library/book/ch01.md"))

    def test_authored_paths_are_not_exempt(self):
        self.assertFalse(chs.is_exempt("docs/standards/writing-style.md"))
        self.assertFalse(chs.is_exempt("tools/build_index.py"))


class CheckFileTests(unittest.TestCase):
    def test_flags_violation_in_a_text_file(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "note.md"
            p.write_text(f"has an em{EMDASH}dash\n", encoding="utf-8")
            self.assertTrue(chs.check_file(str(p)))

    def test_skips_binary_extension(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "art.png"          # not a text extension
            p.write_text(f"em{EMDASH}dash in a non-text file\n", encoding="utf-8")
            self.assertEqual(chs.check_file(str(p)), [])


if __name__ == "__main__":
    unittest.main()
