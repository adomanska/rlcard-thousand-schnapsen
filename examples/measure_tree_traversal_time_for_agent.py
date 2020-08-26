from progressbar import progressbar
from rlcard.envs import Env
import tensorflow as tf
tf.get_logger().setLevel('INFO')

from rlcard_thousand_schnapsen.agents import DeepCFR
from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.utils.analytics import measure_deep_cfr_traversal_time

if __name__ == "__main__":
    with tf.Session() as sess:
        N = 100
        total_elapsed_time = 0
        env: Env = make('thousand-schnapsen',
                        config={
                            'seed': 0,
                            'allow_step_back': True
                        })
        for i in progressbar(range(N)):
            for player_id in range(3):
                agent = DeepCFR(sess,
                                scope=f'deep_cfr_{player_id}_{i}',
                                env=env)
                init_state, _ = env.reset()
                print('TRAVERSAL START')
                elapsed_time = measure_deep_cfr_traversal_time(
                    agent, init_state, player_id)
                total_elapsed_time += elapsed_time
        print(total_elapsed_time / N)
