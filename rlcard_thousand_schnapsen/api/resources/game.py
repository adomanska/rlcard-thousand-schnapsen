from flask import request
from flask_restful import Resource

from rlcard_thousand_schnapsen.api.models import GameSetup
from rlcard_thousand_schnapsen.envs import make


class Game(Resource):
    def __init__(self, model: str):
        self._model = model
        self._env = make('thousand-schnapsen',
                         config={
                             'seed': 0,
                             'force_zero_sum': False
                         })

    def get(self):
        return {'hello': self._model}

    def post(self):
        game_setup: GameSetup = GameSetup.from_dict(request.json)
        print(game_setup.player_types)
        return {}, 200
