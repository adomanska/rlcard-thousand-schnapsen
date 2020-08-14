from typing import List, Tuple, Sequence

import numpy as np

from rlcard.core import Judger, Card

from rlcard_thousand_schnapsen.core import Suit
from .player import ThousandSchnapsenPlayer as Player


class ThousandSchnapsenJudger(Judger):
    """ The Judger class for Thousand Schnapsen
    """
    def __init__(self, np_random: np.random.RandomState):
        self.np_random = np_random

    def judge_round(self, stock: List[Tuple[int, Card]],
                    active_marriage: Suit) -> Tuple[int, int]:
        pass

    def judge_game(self, players: Sequence[Player]) -> Sequence[int]:
        pass
