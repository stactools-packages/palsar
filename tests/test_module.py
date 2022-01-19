import unittest

import stactools.palsar


class TestModule(unittest.TestCase):

    def test_version(self):
        self.assertIsNotNone(stactools.palsar.__version__)
