from typing import Dict, List, Sequence, Tuple, Optional, Set

import numpy as np
from rlcard.envs import Env

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_PER_SUIT_COUNT, CARDS_COUNT, SUITS_COUNT
from rlcard_thousand_schnapsen.utils import Card


class ThousandSchnapsenEnv(Env):
    """ Thousand Schnapsen Environment """
    def __init__(self, config: Dict):
        self.name = 'thousand-schnapsen'
        self.game = Game()
        self.state_shape = [6 * CARDS_COUNT + 2 * SUITS_COUNT]
        super().__init__(config)

    def get_payoffs(self):
        """ Get the payoff of a game
        Returns:
           payoffs (list): list of payoffs
        """
        return self.game.get_payoffs()

    def get_perfect_information(self) -> Dict:
        """ Get the perfect information of the current state
        Return:
            (dict): A dictionary of all the perfect information of the current state
        """
        return self.game.get_perfect_information()

    def _load_model(self):
        pass

    def _extract_state(self, state):
        stock: List[Tuple[int, Card]] = state['stock']
        current_player: int = state['current_player']
        hand: List[Card] = state['hand']
        players_used: Sequence[List[Card]] = state['players_used']
        active_marriage: Optional[str] = state['active_marriage']
        used_marriages: Set[str] = state['used_marriages']

        first_player_id = stock[0][0] if len(stock) > 0 else current_player
        opponents_indices = [
            (first_player_id + i) % self.game.get_player_num()
            for i in range(self.game.get_player_num())
        ]
        opponents_indices = [
            player_id for player_id in opponents_indices
            if player_id != current_player
        ]

        obs = np.zeros(self.state_shape[0], dtype=int)
        start_index = 0
        start_index = self._encode(obs, self._encode_cards_set(hand),
                                   start_index, CARDS_COUNT)
        start_index = self._encode(
            obs, self._encode_cards_set(players_used[current_player]),
            start_index, CARDS_COUNT)
        start_index = self._encode(
            obs, self._encode_cards_set(players_used[opponents_indices[0]]),
            start_index, CARDS_COUNT)
        start_index = self._encode(
            obs, self._encode_cards_set(players_used[opponents_indices[1]]),
            start_index, CARDS_COUNT)
        start_index = self._encode(
            obs, self._encode_card(stock[0][1] if len(stock) > 0 else None),
            start_index, CARDS_COUNT)
        start_index = self._encode(
            obs, self._encode_card(stock[1][1] if len(stock) > 1 else None),
            start_index, CARDS_COUNT)
        start_index = self._encode(obs, self._encode_marriage(active_marriage),
                                   start_index, SUITS_COUNT)
        self._encode(obs, self._encode_marriages(used_marriages), start_index,
                     SUITS_COUNT)

        return {'obs': obs, 'legal_actions': self._get_legal_actions()}

    def _decode_action(self, action_id):
        """ Decode Action id to the action in the game.

        Arg:
            action_id (int): The id of the action

        Return:
            (Card): The action that will be passed to the game engine.
        """
        suit = Card.valid_suit[action_id // CARDS_PER_SUIT_COUNT]
        rank = Card.valid_rank[action_id % CARDS_PER_SUIT_COUNT]
        return Card(suit, rank)

    def _get_legal_actions(self) -> List[int]:
        """ Get all legal actions for current state.
        Returns:
            (list): A list of legal actions' id.
        """
        return [action.__hash__() for action in self.game.get_legal_actions()]

    def _encode(self, code: np.array, chunk: np.array, start_index: int,
                length: int) -> int:
        end_index = start_index + length
        code[start_index:end_index] = chunk
        return end_index

    def _encode_cards_set(self, cards: Sequence[Card]) -> np.array:
        cards_indices = [card.__hash__() for card in cards]
        code = np.zeros(CARDS_COUNT, dtype=int)
        code[cards_indices] = 1
        return code

    def _encode_card(self, card: Optional[Card]) -> np.array:
        code = np.zeros(CARDS_COUNT, dtype=int)
        if card is None:
            return code
        card_index = card.__hash__()
        code[card_index] = 1
        return code

    def _encode_marriages(self, suits: Set[str]) -> np.array:
        suits_indices = [Card.valid_suit.index(suit) for suit in suits]
        code = np.zeros(SUITS_COUNT, dtype=int)
        code[suits_indices] = 1
        return code

    def _encode_marriage(self, suit: Optional[str]) -> np.array:
        code = np.zeros(SUITS_COUNT, dtype=int)
        if suit is None:
            return code
        suit_index = Card.valid_suit.index(suit)
        code[suit_index] = 1
        return code
