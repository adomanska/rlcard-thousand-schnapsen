from enum import Enum
from typing import Tuple, NamedTuple, Any, Optional

from rlcard.core import Card

from rlcard_thousand_schnapsen.core import Suit


class ActionType(Enum):
    PutCard = 'PUT_CARD'
    ActivateMarriage = 'ACTIVATE_MARRIAGE'
    EvaluateRound = 'EVALUATE_ROUND'


class Action:
    type: ActionType
    data: Any


class PutCardAction(NamedTuple, Action):
    data: Tuple[int, Card]
    type = ActionType.PutCard


class ActivateMarriageAction(NamedTuple, Action):
    data: Tuple[Optional[Suit], Suit]
    type = ActionType.ActivateMarriage


class EvaluateRoundAction(NamedTuple, Action):
    data: Tuple[int, int]
    type = ActionType.PutCard
