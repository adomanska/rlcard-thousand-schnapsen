from enum import Enum


class Suit(Enum):
    Spades = 'S'
    Clubs = 'C'
    Diamonds = 'D'
    Hearts = 'H'


class Rank(Enum):
    Nine = '9'
    Ten = 'T'
    Jack = 'J'
    Queen = 'Q'
    King = 'K'
    Ace = 'A'
