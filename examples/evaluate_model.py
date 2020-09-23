import click
import tensorflow as tf
import matplotlib.pyplot as plt
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed
from rlcard_thousand_schnapsen.agents import DeepCFR

from rlcard_thousand_schnapsen.utils import tournament
from rlcard_thousand_schnapsen.envs import make

plt.style.use('ggplot')


@click.command()
@click.option('--path', required=True, help='Path to model')
@click.option('--num', default=1000, help='Number of iterations')
@click.option('--position', default=0, help='Player position')
@click.option('--opponent', default='random', help='Opponent strategy (random or deep_cfr)')
def run(path: str, num: int, position: int, opponent: str):
    # Set a global seed
    set_global_seed(123)

    env = make('thousand-schnapsen',
               config={
                   'seed': 0,
                   'force_zero_sum': True
               })
    agents = []
    for _ in range(env.player_num):
        agent = RandomAgent(action_num=env.action_num)
        agents.append(agent)

    graph = tf.Graph()
    sess = tf.Session(graph=graph)

    with graph.as_default():
        agent = DeepCFR(sess,
                        scope=f'deep_cfr{position}',
                        env=env,
                        policy_network_layers=(8 * 24, 4 * 24, 2 * 24, 24),
                        advantage_network_layers=(8 * 24, 4 * 24, 2 * 24, 24))
        if opponent == 'deep_cfr':
            agents[0] = agent
            agents[1] = agent
            agents[2] = agent
        else:
            agents[position] = agent

    with sess.as_default():
        with graph.as_default():
            saver = tf.train.Saver()
            saver.restore(sess, tf.train.latest_checkpoint(path))

    env.set_agents(agents)
    _, wins = tournament(env, num)
    print(wins)


if __name__ == '__main__':
    run()
