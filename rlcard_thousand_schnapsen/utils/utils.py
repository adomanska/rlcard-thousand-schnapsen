from rlcard.core import Card as BaseCard

CARDS_IN_SUIT_COUNT = 6


class Card(BaseCard):
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
