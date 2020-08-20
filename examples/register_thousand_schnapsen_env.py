from progressbar import progressbar
from rlcard.envs import Env

from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.utils.analytics import measure_traversal_time, TraversalMode

if __name__ == "__main__":
    N = 100
    total_elapsed_time = 0
    total_nodes_count = 0
    env: Env = make('thousand-schnapsen',
                    config={
                        'seed': 0,
                        'allow_step_back': True
                    })
    for _ in progressbar(range(N)):
        for player_id in range(3):
            env.reset()
            elapsed_time, nodes = measure_traversal_time(
                env, TraversalMode.MonteCarlo, player_id)
            total_elapsed_time += elapsed_time
            total_nodes_count += nodes
    print(total_elapsed_time / N, total_nodes_count / N)
