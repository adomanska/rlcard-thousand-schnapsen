import numpy as np

from rlcard.core import Dealer


class ThousandSchnapsenDealer(Dealer):
    """ The Dealer class for Thousand Schnapsen
    """
    def __init__(self, np_random: np.random.RandomState):
        self.np_random = np_random

    def shuffle(self):
        pass

    def deal_cards(self, **kwargs):
        pass
