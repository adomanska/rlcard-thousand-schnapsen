from typing import List, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from .card import Card


@dataclass_json
@dataclass
class GameState:
    stack: List[Card]
    hand: List[Card]
    available_actions: Optional[List[Card]]
    next_player_id: int
    player_id: int
    player_names: List[str]
    points: List[int]
    used_marriages: List[str]
    active_marriage: Optional[str]
    game_over: bool
