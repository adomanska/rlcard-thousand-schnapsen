from abc import ABC
from typing import Sequence, Any, Generic, TypeVar

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

T = TypeVar('T')


class LegalActionsGame(Game, ABC, Generic[T]):
    def get_legal_actions(self) -> Sequence[T]:
        pass
