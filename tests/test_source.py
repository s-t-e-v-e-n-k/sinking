import pathlib
import unittest

from sinking.options import Options
from sinking.source import SourceFile


class TestSourceFile(unittest.TestCase):
    def setUp(self):
        self.options = Options()
        self.options.excludes = []
        self.options.includes = []
        self.options.rename = True

    def tearDown(self):
        self.options.clear()

    def test_name(self):
        s = SourceFile(pathlib.Path("/foo/bar/baz/baz"))
        self.assertEqual(s.name, "baz")
        self.assertFalse(s.needs_rename)

    def test_name_with_rename_false(self):
        self.options.rename = False
        s = SourceFile(pathlib.Path("/foo/bar/baz/bar"))
        self.assertEqual(s.name, "bar")

    def test_needs_rename(self):
        s = SourceFile(pathlib.Path("/foo/bar/baz/foo"))
        self.assertEqual(s.name, "baz")
        self.assertTrue(s.needs_rename)

    def test_pattern_no_season(self):
        s = SourceFile(pathlib.Path("/foo/foo"))
        self.assertEqual(s.pattern, "")

    def test_pattern_with_season(self):
        s = SourceFile(pathlib.Path("/foo/FooBar.S04E19/FooBar.S04E19.Quux"))
        self.assertEqual(s.pattern, "FooBar.S04E")

    def test_default_destination_is_cwd(self):
        s = SourceFile(pathlib.Path("/foo/bar/baz"))
        self.assertEqual(s.destination, pathlib.Path(""))

    def test_destination_can_be_set(self):
        dest = pathlib.Path("/dev")
        s = SourceFile(pathlib.Path("/foo/bar/baz"))
        s.destination = dest
        self.assertEqual(s.destination, dest)

    def test_excluded_sample(self):
        s = SourceFile(
            pathlib.Path("/foo/bar/Foo.S01E02/Foo.S01E02.sample.mkv")
        )
        self.assertTrue(s.excluded)

    def test_excluded_single_excludes(self):
        self.options.excludes = ["Quux"]
        s = SourceFile(pathlib.Path("/foo/bar/Baz.S01E04/Baz.S01E04.mkv"))
        e = SourceFile(pathlib.Path("/foo/bar/Quux.S07E04/Quux.S07E04.mkv"))
        self.assertFalse(s.excluded)
        self.assertTrue(e.excluded)

    def test_excluded_multiple_excludes(self):
        self.options.excludes = ["Quux", "Blah"]
        s = SourceFile(pathlib.Path("/foo/bar/Baz.S01E04/Baz.S01E04.mkv"))
        e1 = SourceFile(pathlib.Path("/foo/bar/Quux.S07E04/Quux.S07E04.mkv"))
        e2 = SourceFile(pathlib.Path("/foo/bar/Blah.S01E01/Blah.S01E01.mkv"))
        self.assertFalse(s.excluded)
        self.assertTrue(e1.excluded)
        self.assertTrue(e2.excluded)

    def test_excluded_single_includes(self):
        self.options.includes = ["Quux"]
        s = SourceFile(pathlib.Path("/foo/bar/Baz.S01E04/Baz.S01E04.mkv"))
        i = SourceFile(pathlib.Path("/foo/bar/Quux.S07E04/Quux.S07E04.mkv"))
        self.assertTrue(s.excluded)
        self.assertFalse(i.excluded)

    def test_excluded_multiple_includes(self):
        self.options.includes = ["Quux", "Blah"]
        s = SourceFile(pathlib.Path("/foo/bar/Baz.S01E04/Baz.S01E04.mkv"))
        i1 = SourceFile(pathlib.Path("/foo/bar/Quux.S07E04/Quux.S07E04.mkv"))
        i2 = SourceFile(pathlib.Path("/foo/bar/Blah.S01E01/Blah.S01E01.mkv"))
        self.assertTrue(s.excluded)
        self.assertFalse(i1.excluded)
        self.assertFalse(i2.excluded)
