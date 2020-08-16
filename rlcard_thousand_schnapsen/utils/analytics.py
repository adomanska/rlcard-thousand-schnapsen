from abc import ABC
from enum import Enum, auto
import time
from typing import Any, Sequence, Optional

import numpy as np

from rlcard.core import Game


class TraversalMode(Enum):
    Complete = auto()
    MonteCarlo = auto()


class LegalActionsGame(Game, ABC):
    def get_legal_actions(self) -> Sequence[Any]:
        pass


def perform_monte_carlo_traversal(game: LegalActionsGame, player_id: int):
    if game.is_over():
        return
    legal_actions = game.get_legal_actions()
    if game.get_player_id() == player_id:
        legal_actions = np.random.choice(legal_actions, 1)

    for action in legal_actions:
        game.step(action)
        perform_monte_carlo_traversal(game, player_id)
        game.step_back()


def perform_complete_traversal(game: LegalActionsGame):
    if game.is_over():
        return
    legal_actions = game.get_legal_actions()

    for action in legal_actions:
        game.step(action)
        perform_complete_traversal(game)
        game.step_back()


def measure_traversal_time(game: LegalActionsGame,
                           mode: TraversalMode,
                           player_id: Optional[int] = None) -> float:
    start = time.time()
    if mode == TraversalMode.MonteCarlo and player_id is not None:
        perform_monte_carlo_traversal(game, player_id)
    if mode == TraversalMode.Complete:
        perform_complete_traversal(game)
    end = time.time()
    return end - start
