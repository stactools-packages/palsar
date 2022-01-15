import unittest

import stactools.stactools_palsar


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.stactools_palsar.__version__)
