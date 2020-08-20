import numpy as np
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
    Spades: np.array([
        0,
    ], dtype=int),
    Clubs: np.array([
        1,
    ], dtype=int),
    Diamonds: np.array([
        2,
    ], dtype=int),
    Hearts: np.array([
        3,
    ], dtype=int),
}

SUIT_SET_CODES = {
    frozenset({}): np.array([], dtype=int),
    frozenset({Spades}): np.array([
        0,
    ], dtype=int),
    frozenset({Clubs}): np.array([
        1,
    ], dtype=int),
    frozenset({Diamonds}): np.array([
        2,
    ], dtype=int),
    frozenset({Hearts}): np.array([
        3,
    ], dtype=int),
    frozenset({Spades, Clubs}): np.array([0, 1], dtype=int),
    frozenset({Spades, Diamonds}): np.array([0, 2], dtype=int),
    frozenset({Spades, Hearts}): np.array([0, 3], dtype=int),
    frozenset({Clubs, Diamonds}): np.array([1, 2], dtype=int),
    frozenset({Clubs, Hearts}): np.array([1, 3], dtype=int),
    frozenset({Diamonds, Hearts}): np.array([2, 3], dtype=int),
    frozenset({Spades, Clubs, Diamonds}): np.array([0, 1, 2], dtype=int),
    frozenset({Spades, Clubs, Hearts}): np.array([0, 1, 3], dtype=int),
    frozenset({Spades, Diamonds, Hearts}): np.array([0, 2, 3], dtype=int),
    frozenset({Clubs, Diamonds, Hearts}): np.array([1, 2, 3], dtype=int),
    frozenset({Spades, Clubs, Diamonds, Hearts}): np.array([0, 1, 2, 3],
                                                           dtype=int)
}

EMPTY_SUIT = np.array([], dtype=int)
