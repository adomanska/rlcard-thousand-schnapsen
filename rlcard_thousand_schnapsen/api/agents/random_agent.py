from time import sleep

from rlcard.agents import RandomAgent as RandomAgentBase


class RandomAgent(RandomAgentBase):
    def eval_step(self, state):
        sleep(1)
        return super().eval_step(state)
