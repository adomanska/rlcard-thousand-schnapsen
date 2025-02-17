import unittest
from copy import copy

import numpy as np

from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from rlcard_thousand_schnapsen.games.thousand_schnapsen.utils import get_marriage_points


class TestGame(unittest.TestCase):
    def test_step(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            action = np.random.choice(list(game.get_legal_actions()))
            game.step(action)
        expected_points_sum = 120 + sum(
            get_marriage_points(marriage) for marriage in game.used_marriages)

        points_sum = np.sum([player.points for player in game.players])

        for player in game.players:
            self.assertEqual(0, len(player.hand))
        self.assertEqual(expected_points_sum, points_sum)
        self.assertEqual(0, len(game.history))

    def test_step_back(self):
        game = Game(allow_step_back=True)
        game.init_game()
        expected_history = []
        while not game.is_over():
            expected_history.append(self._get_game_snapshot(game))
            action = np.random.choice(list(game.get_legal_actions()))
            game.step(action)

        while game.step_back():
            expected_state = expected_history.pop()
            self.assertEqual(expected_state, self._get_game_snapshot(game))

    @staticmethod
    def _get_game_snapshot(game: Game):
        snap = {
            'points': [player.points for player in game.players],
            'hands': [set(player.hand) for player in game.players],
            'used': [set(player.used) for player in game.players],
            'stock': copy(game.stock),
            'used_marriages': copy(game.used_marriages),
            'active_marriage': copy(game.active_marriage),
            'game_pointer': game.game_pointer,
            'round_counter': game.round_counter
        }
        return snap
