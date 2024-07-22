import argparse
import logging
import pathlib
import tempfile
import unittest
from unittest import mock

from sinking.cli import Copier, main
from sinking.options import Options
from sinking.source import SourceFile

from .helpers import create_file_in_dir


class TestMain(unittest.TestCase):
    def test_main(self):
        args = argparse.Namespace(
            no_act=True,
            source=pathlib.Path("/foo/bar"),
            destination=pathlib.Path("/bar/foo"),
            pattern="",
            verbose=False,
        )
        with mock.patch(
            "argparse.ArgumentParser.parse_args", return_value=args
        ):
            ret = main()
        self.assertEqual(ret, 0)
        options = Options()
        self.assertTrue(options.no_act)


class TestCopy(unittest.TestCase):
    def setUp(self):
        self.source = tempfile.TemporaryDirectory()
        self.destination = tempfile.TemporaryDirectory()
        self.options = Options()
        args = {
            "no_act": True,
            "source": pathlib.Path(self.source.name),
            "destination": pathlib.Path(self.destination.name),
            "pattern": "*.bar",
            "includes": [],
            "excludes": [],
            "rename": True,
        }
        for key in args:
            setattr(self.options, key, args.get(key))

    def tearDown(self):
        self.source.cleanup()
        self.destination.cleanup()
        self.options.clear()

    def test_copy_empty_dir(self):
        c = Copier()
        c.copy()
        self.assertEqual(list(c.sources), [])

    def test_copy_no_rename(self):
        name = "Foo.Bar.S01E04.Baz"
        filename = create_file_in_dir(self.options.source, name)
        s = SourceFile(filename)
        c = Copier()
        c.copy()
        self.assertEqual([s.path for s in c.sources], [s.path])

    def test_copy_with_rename(self):
        name = "7y6206u72m"
        dirname = "Foo.Bar.S01E06"
        filename = create_file_in_dir(self.options.source, name, dirname)
        s = SourceFile(filename)
        c = Copier()
        c.copy()
        self.assertEqual([s.path for s in c.sources], [s.path])

    def test_copy_with_rename_acting(self):
        self.options.no_act = False
        name = "v5623jgjf"
        dirname = "Bar.S07E07"
        tmpname = "tmp.n5672fbg"
        _ = create_file_in_dir(self.options.source, name, dirname)
        _ = create_file_in_dir(
            self.options.destination, "Bar.S07E01", tmpname
        )
        c = Copier()
        c.copy()
        newfile = self.options.destination / tmpname / f"{dirname}.bar"
        self.assertTrue(newfile.is_file())

    def test_copy_path_exists(self):
        self.options.no_act = False
        name = "Foo.Bar.S01E04.Baz"
        filename = create_file_in_dir(self.options.source, name)
        s = SourceFile(filename)
        c = Copier()
        c.copy()
        with self.assertLogs(None, level=logging.DEBUG) as cm:
            c.copy()
        output = [
            f"DEBUG:root:Considering {filename}",
            f"DEBUG:root:{s.name} already exists",
        ]
        self.assertEqual(cm.output, output)

    def test_logging(self):
        name = "Quux.S04E03"
        dirname = "tmp.7nfqwnfg"
        filename = create_file_in_dir(self.options.source, name)
        tmpname = self.options.destination / dirname
        _ = create_file_in_dir(
            self.options.destination, "Quux.S04E02", dirname
        )
        with self.assertLogs(None, level=logging.DEBUG) as cm:
            c = Copier()
            c.copy()
        output = [
            f"DEBUG:root:Considering {filename}",
            f"DEBUG:root:Setting destination of {name}.bar to {tmpname}",
            f"INFO:root:{name}.bar -> {dirname} [1/1]",
        ]
        self.assertEqual(cm.output, output)

    def test_copy_with_exclusion(self):
        name = "Foo.Bar.S01E04.Baz"
        _ = create_file_in_dir(self.options.source, f"{name}.sample", name)
        c = Copier()
        c.copy()
        self.assertEqual(list(c.sources), [])
