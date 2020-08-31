from threading import Thread, Event
from typing import List, Callable, Dict

from rlcard_thousand_schnapsen.envs.thousand_schnapsen import ThousandSchnapsenEnv
from rlcard_thousand_schnapsen.api.mappers import env_state_to_game_state


class GameThread(Thread):
    def __init__(self, env: ThousandSchnapsenEnv, human_player_id: int,
                 player_names: List[str], emit: Callable[[str, Dict], None]):
        super(GameThread, self).__init__()
        self._manual_stop = Event()
        self._env = env
        self._human_player_id = human_player_id
        self._player_names = player_names
        self._emit = emit

    def stop(self):
        self._manual_stop.set()

    def manually_stopped(self):
        return self._manual_stop.isSet()

    def run(self):
        state, player_id = self._env.reset()
        self._send_state_update()
        while not self._env.is_over():
            if self.manually_stopped():
                return
            result = self._env.agents[player_id].eval_step(state)
            if result is not None:
                action, _ = result
                state, player_id = self._env.step(action)
                self._send_state_update()

    def _send_state_update(self):
        game_state = env_state_to_game_state(
            state=self._env.state,
            player_id=self._human_player_id,
            player_names=self._player_names,
            game_over=self._env.is_over(),
            legal_actions=self._env.get_legal_actions())
        self._emit('game_state_update', game_state.to_dict())
