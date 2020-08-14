import numpy as np

from rlcard.core import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Dealer
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Player
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Judger


class ThousandSchnapsenGame(Game):
    """ The Game class for Thousand Schnapsen
    """
    dealer = None
    players = None
    judger = None

    def __init__(self):
        """ Initialize the class ThousandSchnapsenGame
        """
        self.np_random = np.random.RandomState()
        self.num_players = 4

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

        # Initialize four players to play the game
        self.players = [
            Player(i, self.np_random) for i in range(self.num_players)
        ]

        # Initialize a judger class which will decide who wins in the end
        self.judger = Judger(self.np_random)

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
