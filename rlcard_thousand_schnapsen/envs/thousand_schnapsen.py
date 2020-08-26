from typing import Dict, List, Sequence, Tuple, Optional, FrozenSet, Union

import numpy as np
from rlcard.envs import Env

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_PER_SUIT_COUNT, CARDS_COUNT, SUITS_COUNT
from rlcard_thousand_schnapsen.utils import Card, init_standard_deck_starting_with_nine
from rlcard_thousand_schnapsen.games.thousand_schnapsen.utils import get_marriage_points
from .utils import OPPONENTS_INDICES


class ThousandSchnapsenEnv(Env):
    """ Thousand Schnapsen Environment """
    def __init__(self, config: Dict):
        self.name = 'thousand-schnapsen'
        self.game = Game()
        self.state_shape = [6 * CARDS_COUNT + 2 * SUITS_COUNT]
        self.history = []
        self.legal_actions = None
        self.possible_cards = None
        self.certain_cards = None
        if 'force_zero_sum' in config:
            self._force_zero_sum = config['force_zero_sum']
        else:
            self._force_zero_sum = False
        super().__init__(config)

    def reset(self):
        self.possible_cards = [
            set(init_standard_deck_starting_with_nine())
            for _ in range(self.player_num)
        ]
        self.certain_cards = [set() for _ in range(self.player_num)]
        return super().reset()

    def step(self, action: int, raw_action=False):
        self._reason_about_cards(action)
        return super().step(action, raw_action)

    def get_payoffs(self):
        """ Get the payoff of a game
        Returns:
           (list): list of payoffs
        """
        payoffs = self.game.get_payoffs()
        if self._force_zero_sum:
            payoffs = np.array(payoffs)
            not_used_marriages = set(
                Card.valid_suit) - self.game.used_marriages
            rest_points = sum([
                get_marriage_points(marriage)
                for marriage in not_used_marriages
            ])
            payoffs += rest_points // self.player_num
            winner = np.argmax(payoffs)
            payoffs[winner] += rest_points % self.player_num
        return payoffs

    def get_perfect_information(self) -> Dict:
        """ Get the perfect information of the current state
        Return:
            (dict): A dictionary of all the perfect information of the current state
        """
        return self.game.get_perfect_information()

    def step_back(self):
        if not self.allow_step_back:
            raise Exception(
                'Step back is off. To use step_back, please set allow_step_back=True in rlcard.make'
            )

        if not self.game.step_back():
            return False

        player_id = self.get_player_id()
        state = self.history.pop()
        self.legal_actions = state['legal_actions']

        return state, player_id

    def _load_model(self):
        pass

    def _extract_state(self, state):
        current_player: int = state['current_player']
        stock: List[Tuple[int, Card]] = state['stock']
        hand: List[Card] = state['hand']
        players_used: Sequence[List[Card]] = state['players_used']
        active_marriage: Optional[str] = state['active_marriage']
        used_marriages: FrozenSet[str] = state['used_marriages']

        first_player_id = stock[0][0] if len(stock) > 0 else current_player
        opponents_indices = self._get_opponents_indices(
            current_player, first_player_id)

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

        self.legal_actions = self._get_legal_actions()
        state = {'obs': obs, 'legal_actions': self.legal_actions}
        self.history.append(state)
        return state

    def _reason_about_cards(self, action: int):
        pass

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

    def _encode(self, code: np.array, chunk: Union[List[int], int],
                start_index: int, length: int) -> int:
        """ Add new chunk to state code
        
        Args:
            code (np.array): Current code
            chunk (Union[List[int], int]): Chunk to be encoded
            start_index (int): Start index
            length (int): Length of chunk
            
        Returns:
            (int): End index
        """
        end_index = start_index + length
        code[start_index:end_index][chunk] = 1
        return end_index

    def _encode_cards_set(self, cards: Sequence[Card]) -> List[int]:
        """ Get chunk encoding cards set
        
        Arg:
            cards (Sequence[Card]): Cards to be encoded
            
        Return:
            (List[int]): Code
        """
        return [card.__hash__() for card in cards]

    def _encode_card(self, card: Optional[Card]) -> Union[List[int], int]:
        """ Get chunk encoding card

        Arg:
            card (Optional[Card]): Card to be encoded

        Return:
            (Union[List[int], int]): Code
        """
        if card is None:
            return []
        return card.__hash__()

    def _encode_marriages(self, suits: FrozenSet[str]) -> List[int]:
        """ Get chunk encoding suits

        Arg:
            suits (FrozenSet[str]): Suits to be encoded

        Return:
            (List[int]): Code
        """
        return [Card.valid_suit.index(suit) for suit in suits]

    def _encode_marriage(self, suit: Optional[str]) -> Union[List[int], int]:
        """ Get chunk encoding suit

        Arg:
            suit (Optional[str]): Card to be encoded

        Return:
            (Union[List[int], int]): Code
        """
        if suit is None:
            return []
        return Card.valid_suit.index(suit)

    def _get_opponents_indices(self, current_player: int,
                               first_player: int) -> Sequence[int]:
        """ Get opponents indices according to current state

        Arg:
            current_player (int): Current player's id
            first_player (int): First player's id

        Return:
            (Sequence[int]): Opponents' ids
        """
        return OPPONENTS_INDICES[first_player][current_player]

    def get_legal_actions(self) -> Sequence[int]:
        """ Get last calculated legal actions
        Return:
           (Sequence[int]): Legal actions
        """
        return self.legal_actions
