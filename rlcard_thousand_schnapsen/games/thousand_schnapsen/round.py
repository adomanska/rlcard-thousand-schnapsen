import numpy as np

from rlcard.core import Round


class ThousandSchnapsenRound(Round):
    """ The Round class for Thousand Schnapsen
    """
    game_pointer: int

    def __init__(self, num_players: int, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenRound class
        """
        self.num_players = num_players
        self.np_random = np_random

    def start_new_round(self, game_pointer: int):
        pass

    def proceed_round(self, **kwargs):
        pass
