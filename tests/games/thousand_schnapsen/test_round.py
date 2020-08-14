import unittest
import numpy as np
from rlcard.core import Card

from rlcard_thousand_schnapsen.core import Suit, Rank
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Round, Player


class TestRound(unittest.TestCase):
    def test_proceed_round(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        game_pointer = 0
        players = [
            Player(player_id, np_random) for player_id in range(num_players)
        ]
        stock = [(2, Card(Suit.Diamonds, Rank.Ten))]
        used_marriages = set()
        card = Card(Suit.Diamonds, Rank.Queen)
        players[game_pointer].hand = [card]
        expected = (1, None)

        result = cur_round.proceed_round(game_pointer, players, stock,
                                         used_marriages, card)

        self.assertEqual(expected, result)
        self.assertEqual((game_pointer, card), stock[1])
        self.assertEqual(0, len(players[game_pointer].hand))

    def test_proceed_round_when_marriage_activated(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        game_pointer = 0
        players = [
            Player(player_id, np_random) for player_id in range(num_players)
        ]
        stock = []
        used_marriages = set()
        card = Card(Suit.Diamonds, Rank.Queen)
        players[game_pointer].hand = [card, Card(Suit.Diamonds, Rank.King)]
        players[game_pointer].points = 0
        expected = (1, Suit.Diamonds)

        result = cur_round.proceed_round(game_pointer, players, stock,
                                         used_marriages, card)

        self.assertEqual(expected, result)
        self.assertEqual((game_pointer, card), stock[0])
        self.assertEqual(80, players[game_pointer].points)
        self.assertEqual(1, len(players[game_pointer].hand))
