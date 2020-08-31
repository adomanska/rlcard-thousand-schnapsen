from typing import Sequence

from rlcard_thousand_schnapsen.api.dto import PlayerType


def get_human_id(player_types: Sequence[PlayerType]) -> int:
    player_id = 0
    while player_id < len(
            player_types) and player_types[player_id] != PlayerType.Human:
        player_id += 1
    return player_id
