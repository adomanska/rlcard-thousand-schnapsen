import unittest
import numpy as np

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Dealer, Player


class TestUtils(unittest.TestCase):
    def test_deal_cards(self):
        np_random = np.random.RandomState()
        player = Player(0, np_random)
        dealer = Dealer(np_random)
        dealer.shuffle()

        dealer.deal_cards(player, 8)

        self.assertEqual(8, len(player.hand))
