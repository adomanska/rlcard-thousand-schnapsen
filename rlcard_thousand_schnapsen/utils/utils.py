import numpy as np
from rlcard.core import Card as BaseCard

CARDS_IN_SUIT_COUNT = 6


class Card(BaseCard):
    """ Card extension for games with deck starting with 9 """
    valid_suit = ['S', 'C', 'D', 'H']
    valid_rank = ['9', 'J', 'Q', 'K', 'T', 'A']

    def __hash__(self) -> int:
        suit_index = Card.valid_suit.index(self.suit)
        rank_index = Card.valid_rank.index(self.rank)
        return rank_index + CARDS_IN_SUIT_COUNT * suit_index


def init_standard_deck_starting_with_nine():
    """ Initialize a standard deck of 24 cards starting with '9'

    Returns:
        (list): A list of Card object
    """
    res = [
        Card(suit, rank) for suit in Card.valid_suit
        for rank in Card.valid_rank
    ]
    return res


def tournament(env, num):
    """ Evaluate he performance of the agents in the environment

    Args:
        env (Env class): The environment to be evaluated.
        num (int): The number of games to play.

    Returns:
        A list of average payoffs for each player
    """
    payoffs = np.zeros(env.player_num, dtype=int)
    counter = 0
    while counter < num:
        _, _payoffs = env.run(is_training=False)
        payoffs += _payoffs
        counter += 1
    for i, _ in enumerate(payoffs):
        payoffs[i] /= counter
    return payoffs
