from threading import Thread, Event

from rlcard.envs import Env


class GameThread(Thread):
    def __init__(self, env: Env):
        super(GameThread, self).__init__()
        self._manual_stop = Event()
        self._env = env

    def stop(self):
        self._manual_stop.set()

    def manually_stopped(self):
        return self._manual_stop.isSet()

    def run(self):
        state, player_id = self._env.reset()
        while not self._env.is_over():
            if self.manually_stopped():
                return
            action, _ = self._env.agents[player_id].eval_step(state)
            print(action)
            state, player_id = self._env.step(action)
