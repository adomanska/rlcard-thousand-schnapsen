from queue import Queue, Empty
from typing import Tuple, Optional


class HumanAgent:
    def __init__(self, action_queue: Queue):
        self._action_queue = action_queue
        self.use_raw = False

    def eval_step(self, state) -> Optional[Tuple[int, int]]:
        try:
            action: int = self._action_queue.get(timeout=0.5)
        except Empty:
            return None
        return action, 0
