from flask import request
from flask_restful import Resource
import tensorflow as tf

from rlcard_thousand_schnapsen.api.dto import GameSetup
from rlcard_thousand_schnapsen.api.utils import load_model, load_agents
from rlcard_thousand_schnapsen.envs import make


class Game(Resource):
    def __init__(self, model: str):
        self._env = make('thousand-schnapsen',
                         config={
                             'seed': 0,
                             'force_zero_sum': False
                         })
        self._model = model
        self._graph = tf.Graph()
        self._sess = tf.Session(graph=self._graph)

    def post(self):
        game_setup: GameSetup = GameSetup.from_dict(request.json)

        if len(game_setup.player_types) < 3:
            return {}, 409

        with self._graph.as_default():
            agents = load_agents(game_setup.player_types, self._env,
                                 self._sess)
            self._env.set_agents(agents)
        load_model(self._graph, self._sess, self._model)
        # TODO: Init game

        return {}, 200
