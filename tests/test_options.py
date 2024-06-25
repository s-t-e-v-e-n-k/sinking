import unittest

from sinking.options import Options


class TestOpions(unittest.TestCase):
    def test_singleton(self):
        o = Options()
        o.data = "blah"
        o2 = Options()
        self.assertEqual(o, o2)
        self.assertEqual(o2.data, "blah")

    def test_clear(self):
        o = Options()
        o.data = "blah"
        o.clear()
        o2 = Options()
        with self.assertRaises(AttributeError):
            o2.data

    def test_can_clear_twice(self):
        o = Options()
        o.clear()
        o.clear()
