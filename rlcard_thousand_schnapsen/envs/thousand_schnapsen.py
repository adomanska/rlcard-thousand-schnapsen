from typing import Dict

from rlcard.envs import Env

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game


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
        pass

    def _get_legal_actions(self):
        pass
