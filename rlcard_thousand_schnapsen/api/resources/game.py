from flask import request
from flask_restful import Resource
import tensorflow as tf

from rlcard_thousand_schnapsen.api.dto import GameSetup, PlayerType
from rlcard_thousand_schnapsen.api.mappers import env_state_to_game_state
from rlcard_thousand_schnapsen.api.utils import load_model, load_agents
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.envs.thousand_schnapsen import ThousandSchnapsenEnv


class Game(Resource):
    def __init__(self, model: str):
        self._env: ThousandSchnapsenEnv = make('thousand-schnapsen',
                                               config={
                                                   'seed': 0,
                                                   'force_zero_sum': False
                                               })
        self._model = model
        self._graph = tf.Graph()
        self._sess = tf.Session(graph=self._graph)
        self._player_id = 0

    def post(self):
        game_setup: GameSetup = GameSetup.from_dict(request.json)

        if len(game_setup.player_types) < 3:
            return {}, 409

        self._player_id = 0
        while game_setup.player_types[self._player_id] != PlayerType.Human:
            self._player_id += 1

        with self._graph.as_default():
            agents = load_agents(game_setup.player_types, self._env,
                                 self._sess)
            self._env.set_agents(agents)
        load_model(self._graph, self._sess, self._model)
        self._env.reset()
        player_names = [
            str(player_type) for player_type in game_setup.player_types
        ]
        game_state = env_state_to_game_state(
            state=self._env.state,
            player_id=self._player_id,
            player_names=player_names,
            game_over=self._env.is_over(),
            legal_actions=self._env.get_legal_actions())

        return game_state.to_dict(), 200
