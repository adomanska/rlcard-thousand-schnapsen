from typing import Sequence, Tuple, List, Set

import numpy as np

from rlcard.core import Round, Card

from .player import ThousandSchnapsenPlayer
from .utils import get_marriage_points
from ...core import Suit, Rank


class ThousandSchnapsenRound(Round):
    """ The Round class for Thousand Schnapsen
    """
    game_pointer: int

    def __init__(self, num_players: int, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenRound class
        """
        self.num_players = num_players
        self.np_random = np_random

    def proceed_round(self, game_pointer: int,
                      players: Sequence[ThousandSchnapsenPlayer],
                      stock: List[Tuple[int, Card]], used_marriages: Set[Suit],
                      card: Card) -> Tuple[int, Suit]:
        activated_marriage = None
        if len(stock) == 0 and self._check_marriage(players[game_pointer],
                                                    card):
            activated_marriage = card.suit
            used_marriages.add(activated_marriage)
            players[game_pointer].points += get_marriage_points(
                activated_marriage)

        stock.append((game_pointer, card))
        players[game_pointer].hand.remove(card)
        next_game_pointer = (game_pointer + 1) % self.num_players
        return next_game_pointer, activated_marriage

    def is_over(self, stock: List[Tuple[int, Card]]) -> bool:
        return len(stock) == self.num_players

    @staticmethod
    def _check_marriage(player: ThousandSchnapsenPlayer, card: Card) -> bool:
        if card.rank == Rank.King and (Card(card.suit, Rank.Queen)
                                       in player.hand):
            return True
        if card.rank == Rank.Queen and (Card(card.suit, Rank.King)
                                        in player.hand):
            return True
        return False
