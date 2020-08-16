from abc import ABC
from typing import Sequence, Any

from rlcard.core import Game

# Suit constants
Spades = 'S'
Clubs = 'C'
Diamonds = 'D'
Hearts = 'H'

# Rank constants
Nine = '9'
Ten = 'T'
Jack = 'J'
Queen = 'Q'
King = 'K'
Ace = 'A'


class LegalActionsGame(Game, ABC):
    def get_legal_actions(self) -> Sequence[Any]:
        pass
