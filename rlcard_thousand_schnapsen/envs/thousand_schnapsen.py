from copy import copy
from typing import Dict, List, Sequence, Tuple, Optional, FrozenSet, Union, Set

import numpy as np
from rlcard.envs import Env

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_PER_SUIT_COUNT, CARDS_COUNT, SUITS_COUNT, \
    PLAYER_COUNT
from rlcard_thousand_schnapsen.utils import Card, init_standard_deck_starting_with_nine
from rlcard_thousand_schnapsen.games.thousand_schnapsen.utils import get_marriage_points, Queen, King, \
    get_context_card_value, get_color
from .utils import OPPONENTS_INDICES


class ThousandSchnapsenEnv(Env):
    """ Thousand Schnapsen Environment """
    def __init__(self, config: Dict):
        self.name = 'thousand-schnapsen'
        self.game = Game()
        self.state_shape = [6 * CARDS_COUNT + 2 * SUITS_COUNT]
        self.history = []
        self.legal_actions = None
        self.possible_cards: Sequence[Set[Card]] = []
        self.certain_cards: Sequence[Set[Card]] = []
        self.state = None
        self.deck = init_standard_deck_starting_with_nine()
        if 'force_zero_sum' in config:
            self._force_zero_sum = config['force_zero_sum']
        else:
            self._force_zero_sum = False
        super().__init__(config)
        self.cards_left = 8 * np.ones(self.player_num)

    def _init_game(self):
        """ Start a new game

        Returns:
            (tuple): Tuple containing:

                (numpy.array): The beginning state of the game
                (int): The beginning player
        """
        self.possible_cards = [
            frozenset(self.deck) for _ in range(self.player_num)
        ]
        self.certain_cards = [frozenset() for _ in range(self.player_num)]
        self.state, player_id = self.game.init_game()
        if self.record_action:
            self.action_recorder = []
        return self._extract_state(self.state), player_id

    def step(self, action: int, raw_action=False):
        if not raw_action:
            action = self._decode_action(action)
        self.timestep += 1
        self.cards_left[self.get_player_id()] -= 1
        next_state, player_id = self.game.step(action)
        self._reason_about_cards(
            action,
            next_state['active_marriage'] != self.state['active_marriage'])
        self.state = next_state
        return self._extract_state(next_state), player_id

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

    def get_reward(self, player: int) -> int:
        return self.state['points'][player]

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
        self.cards_left[player_id] += 1
        self.state, extracted_state, self.certain_cards, self.possible_cards = self.history.pop(
        )
        self.legal_actions = extracted_state['legal_actions']

        return extracted_state, player_id

    def _load_model(self):
        pass

    def _extract_state(self, state):
        current_player: int = state['current_player']
        stock: List[Tuple[int, Card]] = state['stock'] if len(
            state['stock']) < PLAYER_COUNT else []
        hand: FrozenSet[Card] = state['hand']
        active_marriage: Optional[str] = state['active_marriage']
        used_marriages: FrozenSet[str] = state['used_marriages']
        players_used = frozenset.union(*state['players_used'])

        first_player_id = stock[0][0] if len(stock) > 0 else current_player
        opponents_indices = self._get_opponents_indices(
            current_player, first_player_id)
        common_possible_cards = (
            self.possible_cards[opponents_indices[0]] -
            hand) & (self.possible_cards[opponents_indices[1]] - hand)
        certain_cards = [
            (self.certain_cards[opponent_id] |
             (self.possible_cards[opponent_id] - hand - common_possible_cards))
            for opponent_id in opponents_indices
        ]

        if len(certain_cards[0]) == self.cards_left[opponents_indices[0]]:
            certain_cards[1] |= common_possible_cards
            common_possible_cards = set()
        if len(certain_cards[1]) == self.cards_left[opponents_indices[1]]:
            certain_cards[0] |= common_possible_cards
            common_possible_cards = set()

        obs = np.zeros(self.state_shape[0], dtype=bool)
        start_index = 0
        start_index = self._encode(obs, self._encode_cards_set(hand),
                                   start_index, CARDS_COUNT)
        start_index = self._encode(
            obs, self._encode_cards_set(common_possible_cards), start_index,
            CARDS_COUNT)
        start_index = self._encode(obs,
                                   self._encode_cards_set(certain_cards[0]),
                                   start_index, CARDS_COUNT)
        start_index = self._encode(obs,
                                   self._encode_cards_set(certain_cards[1]),
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

        first_card = stock[0][1] if len(stock) > 0 else None
        second_card = stock[1][1] if len(stock) > 1 else None
        is_marriage_crucial = active_marriage is not None and (len([card for card in players_used if card.suit == active_marriage]) < 6 or (first_card is not None and first_card.suit == active_marriage) or (second_card is not None and second_card.suit == active_marriage))
        marriage_hash = active_marriage if(is_marriage_crucial) else None
        hash = (players_used, current_player, marriage_hash, first_card, second_card, used_marriages)

        state = {'obs': obs, 'legal_actions': self.legal_actions, 'hash': hash}
        if self.allow_step_back:
            self.history.append((self.state, state, copy(self.certain_cards),
                                 copy(self.possible_cards)))
        return state

    def _reason_about_cards(self, action: Card, trump: bool):
        current_player = self.get_player_id()
        for i in range(self.player_num):
            self.possible_cards[i] -= {action}
            self.certain_cards[i] -= {action}

        self.possible_cards[current_player] -= self._get_impossible_cards(
            action)

        if trump:
            second_marriage_part = Card(action.suit,
                                        King if action.rank == Queen else King)
            self.certain_cards[current_player] |= {second_marriage_part}
        if len(self.state['stock']) == 0 and not trump and action.rank in {
                Queen, King
        }:
            second_marriage_part = Card(action.suit,
                                        King if action.rank == Queen else King)
            self.possible_cards[current_player] -= {second_marriage_part}

    def _get_impossible_cards(self, action: Card):
        stock = self.state['stock'] if len(
            self.state['stock']) < PLAYER_COUNT else []
        active_marriage = self.state['active_marriage']
        if len(stock) == 0:
            return set()

        first_stock_card_suit = stock[0][1].suit
        max_context_value = max([
            get_context_card_value(card, first_stock_card_suit,
                                   active_marriage) for _, card in stock
        ])
        action_context_value = get_context_card_value(action,
                                                      first_stock_card_suit,
                                                      active_marriage)

        if action.suit == first_stock_card_suit and action_context_value > max_context_value:
            return set()

        suit_cards = get_color(first_stock_card_suit)

        if action.suit != first_stock_card_suit and action_context_value > max_context_value:
            return suit_cards

        greater_cards = {
            card
            for card in self.deck
            if get_context_card_value(card, first_stock_card_suit,
                                      active_marriage) > max_context_value
        }

        if action.suit == first_stock_card_suit and action_context_value < max_context_value:
            return greater_cards & suit_cards

        return greater_cards | suit_cards

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

    def _encode_cards_set(
            self, cards: Union[Set[Card], FrozenSet[Card]]) -> List[int]:
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
