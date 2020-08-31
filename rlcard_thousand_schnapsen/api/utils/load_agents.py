from typing import Sequence, Union

from rlcard.agents import RandomAgent
from rlcard.envs import Env
import tensorflow as tf

from rlcard_thousand_schnapsen.agents import DeepCFR
from rlcard_thousand_schnapsen.api.dto import PlayerType
from .human_agent import HumanAgent


def load_agent(player_type: PlayerType, index: int, env: Env,
               sess: tf.Session) -> Union[HumanAgent, DeepCFR, RandomAgent]:
    if player_type == PlayerType.Human:
        return HumanAgent(env.action_num)
    if player_type == PlayerType.DeepCfr:
        return DeepCFR(sess, scope='deep_cfr' + str(index), env=env)
    return RandomAgent(env.action_num)


def load_agents(player_types: Sequence[PlayerType], env: Env,
                sess: tf.Session):
    return [
        load_agent(player_type, index, env, sess)
        for index, player_type in enumerate(player_types)
    ]
