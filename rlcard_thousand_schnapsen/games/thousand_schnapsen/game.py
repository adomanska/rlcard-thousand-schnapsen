from copy import copy
from typing import List, Tuple, Optional, Set, Dict, Sequence

import numpy as np

from rlcard_thousand_schnapsen.core import LegalActionsGame
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Dealer
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Player
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Judger
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Round
from rlcard_thousand_schnapsen.games.thousand_schnapsen.constants import CARDS_PER_PLAYER_COUNT, ROUNDS_COUNT,\
    CARDS_COUNT
from rlcard_thousand_schnapsen.games.thousand_schnapsen.utils import PutCardAction, ActivateMarriageAction,\
    EvaluateRoundAction, Action, ActionType, get_marriage_points
from rlcard_thousand_schnapsen.utils import Card


class ThousandSchnapsenGame(LegalActionsGame[Card]):
    """ The Game class for Thousand Schnapsen
    """
    dealer: Dealer
    players: List[Player]
    judger: Judger
    game_pointer: int
    round: Round
    round_counter: int
    history: List[Action]
    stock: List[Tuple[int, Card]]
    active_marriage: Optional[str]
    used_marriages: Set[str]

    def __init__(self, allow_step_back: bool = False):
        """ Initialize the class ThousandSchnapsenGame
        """
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 3

    def init_game(self) -> Tuple[Dict, int]:
        """ Initialize the game of Thousand Schnapsen
        
        This version supports three-player and four-players Thousand Schnapsen game
        (in four-player version dealer sits)
        
        Returns:
            (tuple): Tuple containing:
                (dict): The first state of the game
                (int): Current player's id
        """
        # Initialize a dealer that can deal cards
        self.dealer = Dealer(self.np_random)

        # Initialize three players to play the game
        self.players = [
            Player(player_id, self.np_random)
            for player_id in range(self.num_players)
        ]

        # Initialize a judger class which will decide who wins in the end
        self.judger = Judger(self.np_random)

        # Shuffle and deal cards
        self.dealer.shuffle()
        for player in self.players:
            self.dealer.deal_cards(player, CARDS_PER_PLAYER_COUNT)
        # Init game state (we assume for now that player with id 0 always starts)
        self.game_pointer = 0
        self.stock = []
        self.active_marriage = None
        self.used_marriages = set()

        # Initialize a round
        self.round = Round(self.num_players, self.np_random)

        # Count the round. There are 8 rounds in each game.
        self.round_counter = 1

        # Save the history of actions for stepping back to the last state.
        self.history = []

        player_state = self.get_state(self.game_pointer)

        return player_state, self.game_pointer

    def step(self, card: Card) -> Tuple[Dict, int]:
        """ Get the next state
        Arg:
            card (Card): A specific action -- selected card to put
        Returns:
            (tuple): Tuple containing:
                (dict): Next player's state
                (int): Next player's id
        """
        # Update state and history
        new_game_pointer, activated_marriage = self.round.proceed_round(
            self.game_pointer, self.players, self.stock, self.used_marriages,
            card)
        self._update_history(PutCardAction((self.game_pointer, card)))
        if activated_marriage is not None:
            self._update_history(
                ActivateMarriageAction(
                    (self.active_marriage, activated_marriage,
                     self.game_pointer)))
            self.active_marriage = activated_marriage
        self.game_pointer = new_game_pointer

        # Check if round is finished and evaluate
        if self.round.is_over(self.stock):
            winner_id, points = self.judger.judge_round(
                self.stock, self.active_marriage)
            self.players[winner_id].points += points
            self.game_pointer = winner_id
            self.round_counter += 1
            self._update_history(
                EvaluateRoundAction((winner_id, points, copy(self.stock))))
            self.stock.clear()

        player_state = self.get_state(self.game_pointer)

        return player_state, self.game_pointer

    def step_back(self) -> bool:
        """ Return to the previous state of the game
        Return:
            (bool): True if the step back is done successfully, otherwise False
        """
        if not self.allow_step_back:
            raise Exception('Step back is not allowed')
        if len(self.history) > 0:
            while True:
                history_action = self.history.pop()
                action_type = history_action.type
                data = history_action.data
                if action_type == ActionType.EvaluateRound:
                    winner_id, points, stock = data
                    self.players[winner_id].points -= points
                    self.stock = stock
                    self.round_counter -= 1
                elif action_type == ActionType.ActivateMarriage:
                    self.active_marriage, activated_marriage, player_id = data
                    self.used_marriages.remove(activated_marriage)
                    self.players[player_id].points -= get_marriage_points(
                        activated_marriage)
                elif action_type == ActionType.PutCard:
                    player_id, card = data
                    self.players[player_id].hand.append(card)
                    self.players[player_id].used.remove(card)
                    self.game_pointer = player_id
                    self.stock.pop()
                    break
            return True
        return False

    def get_player_num(self) -> int:
        """ Return the number of players in Thousand Schnapsen
        Return:
            (int): The number of players in the game
        """
        return self.num_players

    def get_action_num(self) -> int:
        """ Return the number of applicable actions
        Return:
            (int): The number of actions. There are 24 actions (every card in deck)
        """
        return CARDS_COUNT

    def get_player_id(self) -> int:
        """ Return the current player's id
       Return:
           (int): Current player's id
       """
        return self.game_pointer

    def is_over(self) -> bool:
        """ Check if the game is over
        Return:
            (boolean): True if the game is over
        """
        return self.round_counter > ROUNDS_COUNT

    def get_state(self, player_id: int) -> Dict:
        """ Return current game state for player with given id
        
        Arg:
            player_id (int): Player's id
            
        Return:
            (dict): Game state for given player
        """
        player_state = self.players[player_id].get_state()
        public_state = self._get_public_state()

        return {**player_state, **public_state}

    def get_perfect_information(self) -> Dict:
        """ Return complete game state (with private information)
        Return:
            (dict): Complete game state
        """
        public_state = self._get_public_state()
        return {
            **public_state, 'players_hand':
            [player.hand for player in self.players]
        }

    def _get_public_state(self) -> Dict:
        """ Return current public game state
        Return:
            (dict): Public game state
        """
        return {
            'current_player': self.game_pointer,
            'players_used': [player.used for player in self.players],
            'stock': self.stock,
            'active_marriage': self.active_marriage,
            'used_marriages': frozenset(self.used_marriages),
        }

    def get_legal_actions(self) -> Sequence[Card]:
        """ Calculate and return legal actions according to Thousand Schnapsen rules
        Return:
            (Sequence[Card]): Cards that can be put on the stock
        """
        actions = self.round.get_legal_actions(self.stock,
                                               self.active_marriage,
                                               self.players[self.game_pointer])
        return actions

    def get_payoffs(self) -> Sequence[int]:
        """ Return the payoffs of the game
        Return:
            (Sequence[int]): Each entry corresponds to the payoff of one player
        """
        return self.judger.judge_game(self.players)

    def _update_history(self, history_item: Action):
        """ Check if history needs to be updated and if yes, do update
        """
        if not self.allow_step_back:
            return
        self.history.append(history_item)


# Run random game simulation
if __name__ == "__main__":
    game = ThousandSchnapsenGame()
    print('New Game')
    state, game_pointer = game.init_game()
    print(game_pointer, state)
    while not game.is_over():
        legal_actions = game.get_legal_actions()
        action = np.random.choice(legal_actions)
        print(game_pointer, action,
              [str(legal_action) for legal_action in legal_actions])
        state, game_pointer = game.step(action)
        print(game_pointer, state)
