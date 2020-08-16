from rlcard_thousand_schnapsen.utils.analytics import measure_traversal_time, TraversalMode
from rlcard_thousand_schnapsen.games.thousand_schnapsen import Game
from progressbar import progressbar

if __name__ == "__main__":
    N = 100
    game = Game()
    total_time = 0
    total_nodes = 0
    for _ in progressbar(range(N)):
        for i in range(3):
            game.init_game()
            elapsed_time, nodes = measure_traversal_time(
                game, TraversalMode.MonteCarlo, i)
            total_time += elapsed_time
            total_nodes += nodes
    print(total_time / N, total_nodes / N)
