from dataclasses import dataclass

from dataclasses_json import dataclass_json
from rlcard_thousand_schnapsen.api.dto import Card


@dataclass_json
@dataclass
class Action:
    playerId: int
    card: Card
