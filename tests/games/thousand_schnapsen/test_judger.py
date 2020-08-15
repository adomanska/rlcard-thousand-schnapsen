import unittest
import numpy as np
from rlcard.core import Card

from rlcard_thousand_schnapsen.core import *
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Judger


class TestJudger(unittest.TestCase):
    def test_judge_round_when_no_active_marriage(self):
        np_random = np.random.RandomState()
        judger = Judger(np_random)
        active_marriage = None
        stock = [(0, Card(Clubs, Ten)), (1, Card(Hearts, Nine)),
                 (2, Card(Clubs, Ace))]
        expected = (2, 21)

        result = judger.judge_round(stock, active_marriage)

        self.assertEqual(expected, result)

    def test_judge_round_when_active_marriage(self):
        np_random = np.random.RandomState()
        judger = Judger(np_random)
        active_marriage = Hearts
        stock = [(0, Card(Clubs, Ten)), (1, Card(Hearts, Nine)),
                 (2, Card(Clubs, Ace))]
        expected = (1, 21)

        result = judger.judge_round(stock, active_marriage)

        self.assertEqual(expected, result)

    def test_judge_round_when_active_marriage_equals_first_card_suit(self):
        np_random = np.random.RandomState()
        judger = Judger(np_random)
        active_marriage = Clubs
        stock = [(0, Card(Clubs, Ten)), (1, Card(Hearts, Nine)),
                 (2, Card(Clubs, Ace))]
        expected = (2, 21)

        result = judger.judge_round(stock, active_marriage)

        self.assertEqual(expected, result)
