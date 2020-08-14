import numpy as np

from rlcard.core import Judger


class ThousandSchnapsenJudger(Judger):
    """ The Judger class for Thousand Schnapsen
    """
    def __init__(self, np_random: np.random.RandomState):
        self.np_random = np_random

    def judge_round(self, **kwargs):
        pass

    def judge_game(self, **kwargs):
        pass
