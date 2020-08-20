from rlcard_thousand_schnapsen.core import *

OPPONENTS_INDICES = {
    0: {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1]
    },
    1: {
        0: [1, 2],
        1: [2, 0],
        2: [1, 0]
    },
    2: {
        0: [2, 1],
        1: [2, 0],
        2: [1, 0]
    }
}

SUIT_CODES = {
    Spades: [0],
    Clubs: [1],
    Diamonds: [2],
    Hearts: [3],
}

SUIT_SET_CODES = {
    frozenset({}): [],
    frozenset({Spades}): [0],
    frozenset({Clubs}): [1],
    frozenset({Diamonds}): [2],
    frozenset({Hearts}): [3],
    frozenset({Spades, Clubs}): [0, 1],
    frozenset({Spades, Diamonds}): [0, 2],
    frozenset({Spades, Hearts}): [0, 3],
    frozenset({Clubs, Diamonds}): [1, 2],
    frozenset({Clubs, Hearts}): [1, 3],
    frozenset({Diamonds, Hearts}): [2, 3],
    frozenset({Spades, Clubs, Diamonds}): [0, 1, 2],
    frozenset({Spades, Clubs, Hearts}): [0, 1, 3],
    frozenset({Spades, Diamonds, Hearts}): [0, 2, 3],
    frozenset({Clubs, Diamonds, Hearts}): [1, 2, 3],
    frozenset({Spades, Clubs, Diamonds, Hearts}): [0, 1, 2, 3]
}

EMPTY_SUIT = []
