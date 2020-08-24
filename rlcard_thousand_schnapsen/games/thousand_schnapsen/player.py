from copy import copy
from typing import Dict, Any

import numpy as np

from rlcard.core import Player


class ThousandSchnapsenPlayer(Player):
    """ The Player class for Thousand Schnapsen
    """
    def __init__(self, player_id: int, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenPlayer class
        """
        super().__init__(player_id)
        self.np_random = np_random
        self.hand = set()
        self.used = set()
        self.points = 0

    def available_order(self):
        pass

    def play(self):
        pass

    def get_state(self) -> Dict[str, Any]:
        """ Return current game state
        Return:
            (dict): Game state
        """
        state = dict()
        state['hand'] = self.hand
        return state
