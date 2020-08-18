from typing import Dict, Any, List, Tuple, Sequence

import numpy as np

from rlcard.core import Player

from rlcard_thousand_schnapsen.utils import Card


class ThousandSchnapsenPlayer(Player):
    """ The Player class for Thousand Schnapsen
    """
    def __init__(self, player_id: int, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenPlayer class
        """
        super().__init__(player_id)
        self.np_random = np_random
        self.hand = []
        self.used = []
        self.points = 0

    def available_order(self):
        pass

    def play(self):
        pass

    def get_state(self) -> Dict[str, Any]:
        state = dict()
        state['cards'] = self.hand
        state['used_cards'] = self.hand
        return state
