import numpy as np

from rlcard.core import Player


class ThousandSchnapsenPlayer(Player):
    """ The Player class for Thousand Schnapsen
    """
    def __init__(self, player_id: int, np_random: np.random.RandomState):
        super().__init__(player_id)
        self.np_random = np_random
        self.hand = []

    def available_order(self):
        pass

    def play(self):
        pass
