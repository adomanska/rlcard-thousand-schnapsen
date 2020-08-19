from typing import Dict

from rlcard.envs import Env

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_PER_SUIT_COUNT
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

    def _get_legal_actions(self):
        pass
