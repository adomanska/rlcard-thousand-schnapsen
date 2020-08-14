import unittest

from rlcard_thousand_schnapsen.utils import init_standard_deck_starting_with_nine


class TestUtils(unittest.TestCase):
    def test_init_standard_deck(self):
        self.assertEqual(24, len(init_standard_deck_starting_with_nine()))
