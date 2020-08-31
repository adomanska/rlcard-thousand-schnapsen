from queue import Queue
from typing import Tuple


class HumanAgent:
    def __init__(self, action_queue: Queue):
        self._action_queue = action_queue
        self.use_raw = False

    def eval_step(self, state) -> Tuple[int, int]:
        action: int = self._action_queue.get()
        return action, 0
