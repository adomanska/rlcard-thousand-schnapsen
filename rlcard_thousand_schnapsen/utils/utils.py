from rlcard.core import Card


def init_standard_deck_starting_with_nine():
    """ Initialize a standard deck of 24 cards starting with '9'

    Returns:
        (list): A list of Card object
    """
    suit_list = ['S', 'H', 'D', 'C']
    rank_list = ['A', '9', 'T', 'J', 'Q', 'K']
    res = [Card(suit, rank) for suit in suit_list for rank in rank_list]
    return res
