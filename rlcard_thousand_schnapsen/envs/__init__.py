""" Register new environments
"""
from rlcard.envs.registration import register, make

register(
    env_id='thousand-schnapsen',
    entry_point=
    'rlcard_thousand_schnapsen.envs.thousand_schnapsen:ThousandSchnapsenEnv',
)
