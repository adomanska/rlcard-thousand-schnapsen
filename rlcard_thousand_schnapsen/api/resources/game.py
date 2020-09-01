from queue import Queue
from typing import List, Callable, Dict

from flask import request
from flask_restful import Resource
import tensorflow as tf

from rlcard_thousand_schnapsen.api.dto import GameSetup, Action
from rlcard_thousand_schnapsen.api.mappers import action_dto_to_env_action
from rlcard_thousand_schnapsen.api.utils import load_model, load_agents, get_human_id, get_player_names, GameThread
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.envs.thousand_schnapsen import ThousandSchnapsenEnv

game_thread = None
action_queue = Queue(maxsize=1)


class Game(Resource):
    _player_id: int
    _player_names = List[str]

    def __init__(self, model: str, emit: Callable[[str, Dict], None]):
        self._env: ThousandSchnapsenEnv = make('thousand-schnapsen',
                                               config={
                                                   'seed': 0,
                                                   'force_zero_sum': False
                                               })
        self._model = model
        self._graph = tf.Graph()
        self._sess = tf.Session(graph=self._graph)
        self._emit = emit

    def post(self):
        game_setup: GameSetup = GameSetup.from_dict(request.json)

        if len(game_setup.playerTypes) < 3:
            return {}, 409

        global game_thread
        global action_queue

        if game_thread is not None:
            game_thread.stop()
            game_thread.join()

        with self._graph.as_default():
            agents = load_agents(game_setup.playerTypes, self._env, self._sess,
                                 action_queue)
            self._env.set_agents(agents)
        load_model(self._graph, self._sess, self._model)

        player_id = get_human_id(game_setup.playerTypes)
        player_names = get_player_names(game_setup.playerTypes)

        game_thread = GameThread(self._env, player_id, player_names,
                                 self._emit)
        game_thread.start()

        return {}, 200

    def put(self):
        action: Action = Action.from_dict(request.json)

        global action_queue
        action_queue.put(action_dto_to_env_action(action))

        return {}, 200
