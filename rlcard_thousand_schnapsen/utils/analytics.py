from enum import Enum, auto
import time
from typing import Optional, Tuple, TypeVar, Union

import numpy as np
from rlcard.envs import Env

from rlcard_thousand_schnapsen.core import LegalActionsGame


class TraversalMode(Enum):
    Complete = auto()
    MonteCarlo = auto()


T = TypeVar('T')


def perform_monte_carlo_traversal(game: Union[LegalActionsGame[T], Env],
                                  player_id: int) -> int:
    if game.is_over():
        return 1
    nodes_count = 0
    legal_actions = game.get_legal_actions()
    if game.get_player_id() != player_id:
        legal_actions = np.random.choice(legal_actions, 1)

    for action in legal_actions:
        game.step(action)
        nodes_count += perform_monte_carlo_traversal(game, player_id)
        game.step_back()
    return nodes_count + 1


def perform_complete_traversal(game: Union[LegalActionsGame[T], Env]) -> int:
    if game.is_over():
        return 1
    nodes_count = 0
    legal_actions = game.get_legal_actions()

    for action in legal_actions:
        game.step(action)
        nodes_count += perform_complete_traversal(game)
        game.step_back()
    return nodes_count + 1


def measure_traversal_time(
        game: Union[LegalActionsGame[T], Env],
        mode: TraversalMode,
        player_id: Optional[int] = None) -> Tuple[float, int]:
    nodes_count = 0
    start = time.time()
    if mode == TraversalMode.MonteCarlo and player_id is not None:
        nodes_count = perform_monte_carlo_traversal(game, player_id)
    if mode == TraversalMode.Complete:
        nodes_count = perform_complete_traversal(game)
    end = time.time()
    return end - start, nodes_count
