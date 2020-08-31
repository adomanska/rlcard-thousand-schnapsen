from typing import List

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from rlcard_thousand_schnapsen.api.dto.player_type import PlayerType


@dataclass_json
@dataclass
class GameSetup:
    player_types: List[PlayerType]
