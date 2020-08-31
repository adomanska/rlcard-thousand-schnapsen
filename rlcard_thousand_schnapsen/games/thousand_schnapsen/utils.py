from enum import Enum
from typing import Tuple, NamedTuple, Optional, Set, List

from rlcard_thousand_schnapsen.core import *
from rlcard_thousand_schnapsen.utils import Card
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
    data: Tuple[Optional[str], str, int]
    type = ActionType.ActivateMarriage


class EvaluateRoundAction(NamedTuple, Action):
    data: Tuple[int, int, List[Tuple[int, Card]]]
    type = ActionType.EvaluateRound


def get_card_value(card: Card) -> int:
    return {Nine: 0, Jack: 2, Queen: 3, King: 4, Ten: 10, Ace: 11}[card.rank]


def get_context_card_value(card: Card, first_card_str: str,
                           active_marriage: Optional[str]) -> int:
    multiplier = 1
    if card.suit == first_card_str:
        multiplier = (MAX_RANK_VALUE + 1)
    if card.suit == active_marriage:
        multiplier = (MAX_RANK_VALUE + 1)**2
    return (get_card_value(card) + 1) * multiplier


def get_marriage_points(suit: str) -> int:
    return {Spades: 40, Clubs: 60, Diamonds: 80, Hearts: 100}[suit]


def get_color(suit: str) -> Set[Card]:
    ranks = ['9', 'J', 'Q', 'K', 'T', 'A']
    return {Card(suit, rank) for rank in ranks}
