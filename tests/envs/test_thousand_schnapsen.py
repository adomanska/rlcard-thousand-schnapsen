import unittest
from unittest.mock import MagicMock

import numpy as np
from ddt import ddt, data, unpack

from rlcard_thousand_schnapsen.core import *
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.utils import Card


@ddt
class TestThousandSchnapsenEnv(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.env = make('thousand-schnapsen', config={'seed': 0})
        self.env.reset()

    @data((2, Card(Spades, Queen)), (19, Card(Hearts, Jack)),
          (10, Card(Clubs, Ten)), (17, Card(Diamonds, Ace)))
    @unpack
    def test_decode_action(self, action_id: int, card: Card):
        decoded_action = self.env._decode_action(action_id)
        self.assertEqual(card, decoded_action)

    def test_get_legal_actions(self):
        self.env.game.get_legal_actions = MagicMock(return_value=[
            Card(Spades, Queen),
            Card(Clubs, Ten),
            Card(Diamonds, Ace),
            Card(Hearts, Jack)
        ])
        expected = [2, 10, 17, 19]

        self.assertEqual(expected, self.env._get_legal_actions())

    def test_encode_cards_set(self):
        cards = [
            Card(Spades, Queen),
            Card(Clubs, Ten),
            Card(Diamonds, Ace),
            Card(Hearts, Jack)
        ]
        expected = [2, 10, 17, 19]

        result = self.env._encode_cards_set(cards)

        self.assertSetEqual(set(expected), set(result))

    def test_encode_card_when_card_is_none(self):
        expected = []

        result = self.env._encode_card(None)

        self.assertSetEqual(set(expected), set(result))

    def test_encode_card_when_card_is_defined(self):
        expected = 10

        result = self.env._encode_card(Card(Clubs, Ten))

        self.assertEqual(expected, result)

    def test_encode_marriage_when_suit_is_none(self):
        expected = []

        result = self.env._encode_marriage(None)

        self.assertSetEqual(set(expected), set(result))

    def test_encode_marriage_when_suit_is_defined(self):
        expected = 2

        result = self.env._encode_marriage(Diamonds)

        self.assertEqual(expected, result)

    def test_encode_marriages(self):
        expected = [1, 3]

        result = self.env._encode_marriages({Clubs, Hearts})

        self.assertSetEqual(set(expected), set(result))

    def test_encode(self):
        code = np.zeros(10, dtype=int)
        chunk = [1, 2]
        start_index = 2
        length = 4
        expected = np.zeros(10, dtype=int)
        expected[[3, 4]] = 1

        end_index = self.env._encode(code, chunk, start_index, length)

        self.assertTrue(np.allclose(expected, code))
        self.assertEqual(6, end_index)

    def test_extract_state_when_round_in_progress(self):
        state = {
            'stock': [(1, Card(Diamonds, Jack))],
            'active_marriage': Hearts,
            'used_marriages': {Hearts, Diamonds},
            'hand': frozenset([Card(Diamonds, Queen),
                               Card(Spades, Nine)]),
            'players_used': [[], [Card(Diamonds, Jack)], []],
            'current_player': 2
        }
        expected = np.zeros(152, dtype=int)
        expected[[0, 14]] = 1  # hand
        expected[24:48] = 1  # common possible
        expected[[24 + 0, 24 + 14]] = 0  # remove hand from possible
        expected[109] = 1  # stock
        expected[147] = 1  # active marriage
        expected[[150, 151]] = 1  # used marriages

        result = self.env._extract_state(state)['obs']

        self.assertTrue(np.allclose(expected, result))

    def test_extract_state_when_new_round(self):
        state = {
            'stock': [(1, Card(Diamonds, Jack)), (1, Card(Diamonds, King)),
                      (1, Card(Diamonds, Ace))],
            'active_marriage':
            Hearts,
            'used_marriages': {Hearts, Diamonds},
            'hand':
            frozenset([Card(Diamonds, Queen),
                       Card(Spades, Nine)]),
            'players_used': [[], [Card(Diamonds, Jack)], []],
            'current_player':
            2
        }
        expected = np.zeros(152, dtype=int)
        expected[[0, 14]] = 1  # hand
        expected[24:48] = 1  # common possible
        expected[[24 + 0, 24 + 14]] = 0  # remove hand from possible
        expected[147] = 1  # active marriage
        expected[[150, 151]] = 1  # used marriages

        result = self.env._extract_state(state)['obs']

        self.assertTrue(np.allclose(expected, result))
