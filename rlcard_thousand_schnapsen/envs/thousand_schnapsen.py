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
        pass

    def get_perfect_information(self):
        pass

    def _load_model(self):
        pass

    def _extract_state(self, state):
        pass

    def _decode_action(self, action_id):
        pass

    def _get_legal_actions(self):
        pass
