from typing import Dict, Sequence, List

from rlcard_thousand_schnapsen.api.dto import GameState, Card as CardDto
from rlcard_thousand_schnapsen.utils import init_standard_deck_starting_with_nine, Card


def map_cards(cards: Sequence[Card]) -> List[CardDto]:
    return [CardDto(rank=card.rank, suit=card.suit) for card in cards]


def env_state_to_game_state(state: Dict, player_id: int,
                            player_names: List[str], game_over: bool,
                            legal_actions: Sequence[int]) -> GameState:
    stack = map_cards([card for _, card in state['stock']])
    hand = map_cards(state['hand'])
    next_player_id = state['current_player']
    points = state['points']
    used_marriages = list(state['used_marriages'])
    active_marriage = state['active_marriage']

    if player_id == next_player_id:
        deck = init_standard_deck_starting_with_nine()
        available_actions = map_cards(
            [deck[action] for action in legal_actions])
    else:
        available_actions = None

    return GameState(stack=stack,
                     hand=hand,
                     available_actions=available_actions,
                     next_player_id=next_player_id,
                     player_id=player_id,
                     points=points,
                     used_marriages=used_marriages,
                     active_marriage=active_marriage,
                     player_names=player_names,
                     game_over=game_over)
