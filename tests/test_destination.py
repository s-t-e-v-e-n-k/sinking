import pathlib
import tempfile
import unittest

from sinking.destination import DestinationMatcher
from sinking.options import Options

from .helpers import create_file_in_dir


class TestDestination(unittest.TestCase):
    def setUp(self):
        self.options = Options()
        self.tempdir = tempfile.TemporaryDirectory()
        self.options.destination = pathlib.Path(self.tempdir.name)
        self.options.no_act = True

    def tearDown(self):
        self.tempdir.cleanup()
        self.options.clear()

    def test_destinations_no_dirs(self):
        d = DestinationMatcher()
        self.assertEqual(d.destinations, {})

    def test_destinations_dirs_exists(self):
        name = "tmp.fi85kfjg"
        _ = create_file_in_dir(self.options.destination, "Foo.S03E07", name)
        d = DestinationMatcher()
        destdir = self.options.destination / name
        self.assertDictEqual(d.destinations, {"Foo.S03E": destdir})
        self.assertEqual(d.match("Foo.S03E"), destdir)

    def test_destinations_no_pattern(self):
        name = "tmp.4gownbgf"
        _ = create_file_in_dir(self.options.destination, "Bar", name)
        d = DestinationMatcher()
        self.assertEqual(d.destinations, {})

    def test_destinations_dirs_nonexistant(self):
        d = DestinationMatcher()
        path = d.match("Quux.S07E")
        self.assertRegex(str(path), r"tmp.[0-9a-zA-Z_]{8}")

    def test_destinations_dirs_nonexistant_acting(self):
        self.options.no_act = False
        d = DestinationMatcher()
        path = d.match("Blah.S01E")
        self.assertIsInstance(path, pathlib.Path)
        self.assertTrue(path.is_dir())
        # We need to touch a file to have it be found
        (path / "Blah.S01E07.bar").touch()
        d = DestinationMatcher()
        second_path = d.match("Blah.S01E")
        self.assertEqual(path, second_path)
