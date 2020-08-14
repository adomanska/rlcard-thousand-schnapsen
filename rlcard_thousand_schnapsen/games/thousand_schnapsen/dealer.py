import numpy as np

from rlcard.core import Dealer

from rlcard_thousand_schnapsen.utils import init_standard_deck_starting_with_nine


class ThousandSchnapsenDealer(Dealer):
    """ The Dealer class for Thousand Schnapsen
    """
    def __init__(self, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenDealer class
        """
        self.np_random = np_random
        self.deck = init_standard_deck_starting_with_nine()

    def shuffle(self):
        """ Shuffle the deck
        """
        self.deck = list(self.np_random.shuffle(self.deck))

    def deal_cards(self, **kwargs):
        pass
