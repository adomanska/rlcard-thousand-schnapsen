from typing import Tuple, Sequence, Optional

import numpy as np

from rlcard.core import Judger

from rlcard_thousand_schnapsen.utils import Card
from .player import ThousandSchnapsenPlayer as Player
from .utils import get_context_card_value, get_card_value


class ThousandSchnapsenJudger(Judger):
    """ The Judger class for Thousand Schnapsen
    """
    def __init__(self, np_random: np.random.RandomState):
        self.np_random = np_random

    def judge_round(self, stock: Sequence[Tuple[int, Card]],
                    active_marriage: Optional[str]) -> Tuple[int, int]:
        """ Judge the winner of the round and count points
       Args:
           stock (Sequence[Tuple[int, Card]]): The stock of cards with players' ids
           active_marriage (Optional[str]): Currently active marriage
       Returns:
           (tuple): Tuple containing:
               (int): Id of the winner
               (int): Points won
       """
        first_card_str = stock[0][1].suit
        cards_context_values = [
            get_context_card_value(card, first_card_str, active_marriage)
            for _, card in stock
        ]
        winner_id = stock[np.argmax(cards_context_values)][0]
        points = np.sum([get_card_value(card) for _, card in stock])
        return winner_id, points

    def judge_game(self, players: Sequence[Player]) -> Sequence[int]:
        """ Judge the winner of the game
        Arg:
            players (Sequence[Player]): The list of players who play the game
        Return:
            (Sequence[int]): Points won by each player
        """
        return [player.points for player in players]
