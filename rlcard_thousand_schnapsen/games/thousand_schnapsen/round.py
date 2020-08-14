from typing import Sequence, Tuple, List, Set

import numpy as np

from rlcard.core import Round, Card

from .player import Player
from ...core import Suit


class ThousandSchnapsenRound(Round):
    """ The Round class for Thousand Schnapsen
    """
    game_pointer: int

    def __init__(self, num_players: int, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenRound class
        """
        self.num_players = num_players
        self.np_random = np_random

    def proceed_round(self, game_pointer: int, players: Sequence[Player],
                      stock: List[Tuple[int, Card]], used_marriages: Set[Suit],
                      card: Card) -> Tuple[int, Suit]:
        pass

    def is_over(self, stock: List[Tuple[int, Card]]) -> bool:
        pass
