from time import sleep

from rlcard_thousand_schnapsen.agents import DeepCFR


class DeepCFRAgent(DeepCFR):
    def eval_step(self, state):
        sleep(1)
        return super().eval_step(state)
