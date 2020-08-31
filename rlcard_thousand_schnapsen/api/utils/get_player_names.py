from typing import Sequence, List, Dict

from rlcard_thousand_schnapsen.api.dto import PlayerType


def get_player_name(player_type: PlayerType, players_count: Dict[PlayerType,
                                                                 int]) -> str:
    if player_type == PlayerType.Human:
        return 'Me'
    player_no = players_count[player_type] + 1
    players_count[player_type] += 1
    if player_type == PlayerType.Random:
        return f'Random #{player_no}'
    if player_type == PlayerType.DeepCfr:
        return f'DeepCfr #{player_no}'


def get_player_names(player_types: Sequence[PlayerType]) -> List[str]:
    players_count = {PlayerType.DeepCfr: 0, PlayerType.Random: 0}

    return [
        get_player_name(player_type, players_count)
        for player_type in player_types
    ]
