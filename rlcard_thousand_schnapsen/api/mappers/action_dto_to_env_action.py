from rlcard_thousand_schnapsen.api.dto.action import Action
from rlcard_thousand_schnapsen.utils import Card


def action_dto_to_env_action(action: Action) -> int:
    card = Card(rank=action.card.rank, suit=action.card.suit)
    return card.__hash__()
