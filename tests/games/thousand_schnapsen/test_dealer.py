import unittest
import numpy as np

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Dealer, Player, ImpossibleCardsDealException


class TestUtils(unittest.TestCase):
    def test_deal_cards(self):
        np_random = np.random.RandomState()
        players = [Player(player_id, np_random) for player_id in range(3)]
        dealer = Dealer(np_random)
        dealer.shuffle()

        for player_id in range(3):
            dealer.deal_cards(players[player_id], 8)
            self.assertEqual(8, len(players[player_id].hand))

        self.assertRaises(ImpossibleCardsDealException,
                          lambda: dealer.deal_cards(players[0], 8))
