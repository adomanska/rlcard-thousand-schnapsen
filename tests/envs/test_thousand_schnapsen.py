import unittest

from ddt import ddt, data, unpack

from rlcard_thousand_schnapsen.core import *
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.utils import Card


@ddt
class TestThousandSchnapsenEnv(unittest.TestCase):
    @data((2, Card(Spades, Queen)), (19, Card(Hearts, Jack)),
          (10, Card(Clubs, Ten)), (17, Card(Diamonds, Ace)))
    @unpack
    def test_decode_action(self, action_id: int, card: Card):
        env = make('thousand-schnapsen', config={'seed': 0})
        decoded_action = env._decode_action(action_id)
        self.assertEqual(card, decoded_action)
