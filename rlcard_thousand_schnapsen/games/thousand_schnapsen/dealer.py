import numpy as np

from rlcard.core import Dealer

from rlcard_thousand_schnapsen.utils import init_standard_deck_starting_with_nine
from .player import Player
from .errors import ImpossibleCardsDealException


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
        shuffled_deck = np.array(self.deck)
        self.np_random.shuffle(shuffled_deck)
        self.deck = list(shuffled_deck)

    def deal_cards(self, player: Player, num: int):
        """ Deal some cards from deck to one player
        Args:
            player (object): The object of ThousandSchnapsenPlayer
            num (int): The number of cards to be dealt
        """
        if len(self.deck) < num:
            raise ImpossibleCardsDealException(len(self.deck), num)
        for _ in range(num):
            player.hand.append(self.deck.pop())
