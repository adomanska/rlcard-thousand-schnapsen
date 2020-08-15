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

    def test_get_legal_actions_when_stock_empty(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = [
            Card(Suit.Spades, Rank.Ten),
            Card(Suit.Diamonds, Rank.Nine),
            Card(Suit.Hearts, Rank.Queen),
            Card(Suit.Spades, Rank.King),
            Card(Suit.Clubs, Rank.Ace),
        ]
        player.hand = cards
        stock = []
        active_marriage = None
        expected = cards

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSequenceEqual(expected, result)

    def test_get_legal_actions_when_can_put_same_suit_and_beat(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = [
            Card(Suit.Spades.value, Rank.Ten.value),
            Card(Suit.Diamonds.value, Rank.Nine.value),
            Card(Suit.Hearts.value, Rank.Queen.value),
            Card(Suit.Spades.value, Rank.Queen.value),
            Card(Suit.Clubs.value, Rank.Ace.value),
        ]
        player.hand = cards
        stock = [(2, Card(Suit.Spades.value, Rank.King.value))]
        active_marriage = None
        expected = [
            Card(Suit.Spades.value, Rank.Ten.value),
        ]

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSequenceEqual(expected, result)

    def test_get_legal_actions_when_can_put_same_suit_but_not_beat(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = [
            Card(Suit.Spades.value, Rank.Ten.value),
            Card(Suit.Diamonds.value, Rank.Nine.value),
            Card(Suit.Hearts.value, Rank.Queen.value),
            Card(Suit.Spades.value, Rank.Queen.value),
            Card(Suit.Clubs.value, Rank.Ace.value),
        ]
        player.hand = cards
        stock = [(2, Card(Suit.Spades.value, Rank.Ace.value))]
        active_marriage = Suit.Hearts.value
        expected = [
            Card(Suit.Spades.value, Rank.Ten.value),
            Card(Suit.Spades.value, Rank.Queen.value),
        ]

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSequenceEqual(expected, result)

    def test_get_legal_actions_when_can_beat_with_active_marriage(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = [
            Card(Suit.Spades.value, Rank.Ten.value),
            Card(Suit.Diamonds.value, Rank.Nine.value),
            Card(Suit.Hearts.value, Rank.Queen.value),
            Card(Suit.Spades.value, Rank.Queen.value),
        ]
        player.hand = cards
        stock = [(2, Card(Suit.Clubs.value, Rank.Ace.value))]
        active_marriage = Suit.Hearts.value
        expected = [
            Card(Suit.Hearts.value, Rank.Queen.value),
        ]

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSequenceEqual(expected, result)

    def test_get_legal_actions_when_cannot_put_same_suit_nor_beat(self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = [
            Card(Suit.Spades.value, Rank.Ten.value),
            Card(Suit.Diamonds.value, Rank.Nine.value),
            Card(Suit.Spades.value, Rank.Queen.value),
        ]
        player.hand = cards
        stock = [(2, Card(Suit.Clubs.value, Rank.Ace.value))]
        active_marriage = Suit.Hearts.value
        expected = cards

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSequenceEqual(expected, result)

    def test_get_legal_actions_when_active_marriage_equal_first_card_suit(
            self):
        num_players = 3
        np_random = np.random.RandomState()
        cur_round = Round(num_players, np_random)
        player = Player(0, np_random)
        cards = [
            Card(Suit.Spades.value, Rank.Ten.value),
            Card(Suit.Diamonds.value, Rank.Nine.value),
            Card(Suit.Spades.value, Rank.Queen.value),
            Card(Suit.Clubs.value, Rank.Ten.value)
        ]
        player.hand = cards
        stock = [(2, Card(Suit.Clubs.value, Rank.Ace.value))]
        active_marriage = Suit.Clubs.value
        expected = [Card(Suit.Clubs.value, Rank.Ten.value)]

        result = cur_round.get_legal_actions(stock, active_marriage, player)

        self.assertSequenceEqual(expected, result)
