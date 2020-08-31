from typing import List, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from .card import Card


@dataclass_json
@dataclass
class GameState:
    stack: List[Card]
    hand: List[Card]
    availableActions: Optional[List[Card]]
    nextPlayerId: int
    playerId: int
    playerNames: List[str]
    points: List[int]
    usedMarriages: List[str]
    activeMarriage: Optional[str]
    gameOver: bool
