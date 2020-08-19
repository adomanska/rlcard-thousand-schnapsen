import unittest
from unittest.mock import MagicMock

import numpy as np
from ddt import ddt, data, unpack

from rlcard_thousand_schnapsen.core import *
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_COUNT
from rlcard_thousand_schnapsen.utils import Card


@ddt
class TestThousandSchnapsenEnv(unittest.TestCase):
    env = make('thousand-schnapsen', config={'seed': 0})

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
        expected = np.zeros(CARDS_COUNT, dtype=int)
        expected[[2, 10, 17, 19]] = 1

        result = self.env._encode_cards_set(cards)

        self.assertTrue(np.allclose(expected, result))
