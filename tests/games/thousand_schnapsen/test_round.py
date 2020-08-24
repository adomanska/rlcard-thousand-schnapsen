import unittest
import numpy as np

from rlcard_thousand_schnapsen.core import *
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Round, Player
from rlcard_thousand_schnapsen.utils import Card


class TestRound(unittest.TestCase):
    def test_proceed_round(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        game_pointer = 0
        players = [
            Player(player_id, np_random) for player_id in range(num_players)
        ]
        stock = [(2, Card(Diamonds, Ten))]
        used_marriages = set()
        card = Card(Diamonds, Queen)
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
        card = Card(Diamonds, Queen)
        players[game_pointer].hand = [card, Card(Diamonds, King)]
        players[game_pointer].points = 0
        expected = (1, Diamonds)

        result = cur_round.proceed_round(game_pointer, players, stock,
                                         used_marriages, card)

        self.assertEqual(expected, result)
        self.assertEqual((game_pointer, card), stock[0])
        self.assertEqual(80, players[game_pointer].points)
        self.assertEqual(1, len(players[game_pointer].hand))

    def test_get_legal_actions_when_stock_empty(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = {
            Card(Spades, Ten),
            Card(Diamonds, Nine),
            Card(Hearts, Queen),
            Card(Spades, King),
            Card(Clubs, Ace),
        }
        player.hand = cards
        stock = []
        active_marriage = None
        expected = cards

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSetEqual(expected, result)

    def test_get_legal_actions_when_can_put_same_suit_and_beat(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = {
            Card(Spades, Ten),
            Card(Diamonds, Nine),
            Card(Hearts, Queen),
            Card(Spades, Queen),
            Card(Clubs, Ace),
        }
        player.hand = cards
        stock = [(2, Card(Spades, King))]
        active_marriage = None
        expected = {
            Card(Spades, Ten),
        }

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSetEqual(expected, result)

    def test_get_legal_actions_when_can_put_same_suit_but_not_beat(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = {
            Card(Spades, Ten),
            Card(Diamonds, Nine),
            Card(Hearts, Queen),
            Card(Spades, Queen),
            Card(Clubs, Ace),
        }
        player.hand = cards
        stock = [(2, Card(Spades, Ace))]
        active_marriage = Hearts
        expected = {
            Card(Spades, Queen),
            Card(Spades, Ten),
        }

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSetEqual(expected, result)

    def test_get_legal_actions_when_can_beat_with_active_marriage(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = {
            Card(Spades, Ten),
            Card(Diamonds, Nine),
            Card(Hearts, Queen),
            Card(Spades, Queen),
        }
        player.hand = cards
        stock = [(2, Card(Clubs, Ace))]
        active_marriage = Hearts
        expected = {
            Card(Hearts, Queen),
        }

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSetEqual(expected, result)

    def test_get_legal_actions_when_cannot_put_same_suit_nor_beat(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = {
            Card(Spades, Ten),
            Card(Diamonds, Nine),
            Card(Spades, Queen),
        }
        player.hand = cards
        stock = [(2, Card(Clubs, Ace))]
        active_marriage = Hearts
        expected = cards

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSetEqual(expected, result)

    def test_get_legal_actions_when_active_marriage_equal_first_card_suit(
            self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = {
            Card(Spades, Ten),
            Card(Diamonds, Nine),
            Card(Spades, Queen),
            Card(Clubs, Ten)
        }
        player.hand = cards
        stock = [(2, Card(Clubs, Ace))]
        active_marriage = Clubs
        expected = {Card(Clubs, Ten)}

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSetEqual(expected, result)
