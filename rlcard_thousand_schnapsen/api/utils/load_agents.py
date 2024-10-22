from queue import Queue
from typing import Sequence, Union, List

from rlcard.envs import Env
import tensorflow as tf

from rlcard_thousand_schnapsen.api.dto import PlayerType
from rlcard_thousand_schnapsen.api.agents import HumanAgent, DeepCFRAgent, RandomAgent

Agent = Union[HumanAgent, DeepCFRAgent, RandomAgent]


def load_agent(player_type: PlayerType, index: int, env: Env, sess: tf.Session,
               action_queue: Queue) -> Agent:
    if player_type == PlayerType.Human:
        return HumanAgent(action_queue)
    if player_type == PlayerType.DeepCfr:
        return DeepCFRAgent(sess, scope='deep_cfr' + str(index), env=env)
    return RandomAgent(env.action_num)


def load_agents(player_types: Sequence[PlayerType], env: Env, sess: tf.Session,
                action_queue: Queue) -> List[Agent]:
    return [
        load_agent(player_type, index, env, sess, action_queue)
        for index, player_type in enumerate(player_types)
    ]
