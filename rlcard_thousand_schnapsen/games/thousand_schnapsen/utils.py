from enum import Enum
from typing import Tuple, NamedTuple, Any, Optional

from rlcard.core import Card

from rlcard_thousand_schnapsen.core import Suit, Rank
from .constants import MAX_RANK_VALUE


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


def get_card_value(card: Card) -> int:
    return {
        Rank.Nine: 0,
        Rank.Jack: 2,
        Rank.Queen: 3,
        Rank.King: 4,
        Rank.Ten: 10,
        Rank.Ace: 11
    }[card.rank]


def get_context_card_value(card: Card, first_card_suite: Suit,
                           active_marriage: Optional[Suit]) -> int:
    multiplier = 1
    if card.suit == first_card_suite:
        multiplier = (MAX_RANK_VALUE + 1)
    if card.suit == active_marriage:
        multiplier = (MAX_RANK_VALUE + 1)**2
    return (get_card_value(card) + 1) * multiplier
