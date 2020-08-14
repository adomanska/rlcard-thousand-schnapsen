from typing import List, Tuple, Optional, Set, Dict

import numpy as np

from rlcard.core import Game, Card

from rlcard_thousand_schnapsen.core import Suit
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Dealer
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Player
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Judger
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Round


class ThousandSchnapsenGame(Game):
    """ The Game class for Thousand Schnapsen
    """
    dealer: Dealer
    players: List[Player]
    judger: Judger
    game_pointer: int
    round: Round
    round_counter: int
    history: List[Dict]
    stock: List[Tuple[int, Card]]
    active_marriage: Optional[Suit]
    used_marriages: Set[Suit]

    def __init__(self):
        """ Initialize the class ThousandSchnapsenGame
        """
        self.np_random = np.random.RandomState()
        self.num_players = 3

    def init_game(self):
        """ Initialize the game of Thousand Schnapsen
        
        This version supports four-player Thousand Schnapsen
        
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

        # Deal cards
        for player in self.players:
            self.dealer.deal_cards(player, 8)
        # Init game state
        # We assume for now that player with id 0 always starts
        self.game_pointer = 0
        self.stock = []
        self.active_marriage = None
        self.used_marriages = set()

        # Initialize a round
        self.round = Round(self.num_players, self.np_random)
        self.round.start_new_round(self.game_pointer)

        # Count the round. There are 8 rounds in each game.
        self.round_counter = 0

        # Save the history for stepping back to the last state.
        self.history = []

        state = self.get_state(self.game_pointer)

        return state, self.game_pointer

    def step(self, action):
        pass

    def step_back(self):
        pass

    def get_player_num(self):
        pass

    def get_action_num(self):
        pass

    def get_player_id(self):
        pass

    def is_over(self):
        pass

    def get_state(self, game_pointer) -> Dict:
        pass
