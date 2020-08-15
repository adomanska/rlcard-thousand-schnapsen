from typing import Sequence, Tuple, List, Set, Optional

import numpy as np

from rlcard.core import Round, Card

from .player import ThousandSchnapsenPlayer
from .utils import get_marriage_points, get_context_card_value, get_color
from ...core import Suit, Rank


class ThousandSchnapsenRound(Round):
    """ The Round class for Thousand Schnapsen
    """
    game_pointer: int

    def __init__(self, num_players: int, np_random: np.random.RandomState):
        """ Initialize a ThousandSchnapsenRound class
        """
        self.num_players = num_players
        self.np_random = np_random

    def proceed_round(self, game_pointer: int,
                      players: Sequence[ThousandSchnapsenPlayer],
                      stock: List[Tuple[int, Card]], used_marriages: Set[Suit],
                      card: Card) -> Tuple[int, Optional[Suit]]:
        """ Call other Classes's functions to keep one round running

        Args:
            game_pointer (int): current player id
            players (Sequence[Player): collection of players
            stock (List[Tuple[(int, Card)]]): stock of cards
            used_marriages (Set[Suit]): set of already used marriages
            card: Card: action to perform

        Returns:
            (int): next player id
            (Optional[Suit]): new active marriage
        """
        activated_marriage = None
        if len(stock) == 0 and self._check_marriage(players[game_pointer],
                                                    card):
            activated_marriage = card.suit
            used_marriages.add(activated_marriage)
            players[game_pointer].points += get_marriage_points(
                activated_marriage)

        stock.append((game_pointer, card))
        players[game_pointer].hand.remove(card)
        next_game_pointer = (game_pointer + 1) % self.num_players
        return next_game_pointer, activated_marriage

    def is_over(self, stock: List[Tuple[int, Card]]) -> bool:
        return len(stock) == self.num_players

    def get_legal_actions(self, stock: List, active_marriage: Optional[Suit],
                          player: ThousandSchnapsenPlayer) -> Sequence[Card]:
        if len(stock) == 0:
            return player.hand

        player_cards = set(player.hand)
        first_stock_card_suit = stock[0][1].suit
        max_context_value = np.max([
            get_context_card_value(card, first_stock_card_suit,
                                   active_marriage) for _, card in stock
        ])
        suit_cards = get_color(first_stock_card_suit) & player_cards
        greater_cards = set([
            card for card in player_cards
            if get_context_card_value(card, first_stock_card_suit,
                                      active_marriage) > max_context_value
        ])

        if len(suit_cards & greater_cards) > 0:
            return list(suit_cards & greater_cards)
        if len(suit_cards) > 0:
            return list(suit_cards)
        if len(greater_cards) > 0:
            return list(greater_cards)
        return player.hand

    @staticmethod
    def _check_marriage(player: ThousandSchnapsenPlayer, card: Card) -> bool:
        if card.rank == Rank.King and (Card(card.suit, Rank.Queen)
                                       in player.hand):
            return True
        if card.rank == Rank.Queen and (Card(card.suit, Rank.King)
                                        in player.hand):
            return True
        return False
