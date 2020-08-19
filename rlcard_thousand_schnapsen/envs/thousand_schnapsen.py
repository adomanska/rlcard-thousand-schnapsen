from typing import Dict, List, Sequence

import numpy as np
from rlcard.envs import Env

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_PER_SUIT_COUNT, CARDS_COUNT
from rlcard_thousand_schnapsen.utils import Card


class ThousandSchnapsenEnv(Env):
    """ Thousand Schnapsen Environment """
    def __init__(self, config: Dict):
        self.name = 'thousand-schnapsen'
        self.game = Game()
        super().__init__(config)

    def get_payoffs(self):
        """ Get the payoff of a game
        Returns:
           payoffs (list): list of payoffs
        """
        return self.game.get_payoffs()

    def get_perfect_information(self) -> Dict:
        """ Get the perfect information of the current state
        Return:
            (dict): A dictionary of all the perfect information of the current state
        """
        return self.game.get_perfect_information()

    def _load_model(self):
        pass

    def _extract_state(self, state):
        pass

    def _decode_action(self, action_id):
        """ Decode Action id to the action in the game.

        Arg:
            action_id (int): The id of the action

        Return:
            (Card): The action that will be passed to the game engine.
        """
        suit = Card.valid_suit[action_id // CARDS_PER_SUIT_COUNT]
        rank = Card.valid_rank[action_id % CARDS_PER_SUIT_COUNT]
        return Card(suit, rank)

    def _get_legal_actions(self) -> List[int]:
        """ Get all legal actions for current state.
        Returns:
            (list): A list of legal actions' id.
        """
        return [action.__hash__() for action in self.game.get_legal_actions()]

    def _encode_cards_set(self, cards: Sequence[Card]) -> np.array:
        cards_indices = [card.__hash__() for card in cards]
        code = np.zeros(CARDS_COUNT, dtype=int)
        code[cards_indices] = 1
        return code
