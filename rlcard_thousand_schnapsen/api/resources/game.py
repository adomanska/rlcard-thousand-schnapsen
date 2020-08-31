from typing import List

from flask import request
from flask_restful import Resource
import tensorflow as tf

from rlcard_thousand_schnapsen.api.dto import GameSetup
from rlcard_thousand_schnapsen.api.mappers import env_state_to_game_state
from rlcard_thousand_schnapsen.api.utils import load_model, load_agents, get_human_id, get_player_names
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.envs.thousand_schnapsen import ThousandSchnapsenEnv


class Game(Resource):
    _player_id: int
    _player_names = List[str]

    def __init__(self, model: str):
        self._env: ThousandSchnapsenEnv = make('thousand-schnapsen',
                                               config={
                                                   'seed': 0,
                                                   'force_zero_sum': False
                                               })
        self._model = model
        self._graph = tf.Graph()
        self._sess = tf.Session(graph=self._graph)

    def post(self):
        game_setup: GameSetup = GameSetup.from_dict(request.json)

        if len(game_setup.playerTypes) < 3:
            return {}, 409

        with self._graph.as_default():
            agents = load_agents(game_setup.playerTypes, self._env,
                                 self._sess)
            self._env.set_agents(agents)
        load_model(self._graph, self._sess, self._model)

        self._player_id = get_human_id(game_setup.playerTypes)
        self._player_names = get_player_names(game_setup.playerTypes)

        self._env.reset()
        game_state = env_state_to_game_state(
            state=self._env.state,
            player_id=self._player_id,
            player_names=self._player_names,
            game_over=self._env.is_over(),
            legal_actions=self._env.get_legal_actions())

        return game_state.to_dict(), 200
