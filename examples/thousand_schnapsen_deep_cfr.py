""" An example of learning a DeepCFR Agent on Thousand Schnapsen
"""

import tensorflow as tf
import os
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed
from rlcard.utils import Logger

from rlcard_thousand_schnapsen.envs import make
from rlcard_thousand_schnapsen.agents import DeepCFR
from rlcard_thousand_schnapsen.utils import tournament

# Make environment
env = make('thousand-schnapsen',
           config={
               'seed': 0,
               'allow_step_back': True,
               'force_zero_sum': True
           })
eval_env = make('thousand-schnapsen',
                config={
                    'seed': 0,
                    'force_zero_sum': True
                })

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 1
evaluate_num = 1000
episode_num = 100000

# The paths for saving the logs and learning curves
log_dir = './experiments/thousand_schnapsen_deep_cfr_result/'

# Set a global seed
set_global_seed(0)

with tf.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agents = []
    random_agents = []
    for i in range(env.player_num):
        agent = DeepCFR(sess,
                        scope='deep_cfr' + str(i),
                        env=env,
                        num_step=30000,
                        learning_rate=1e-5,
                        memory_capacity=int(1e6))
        agents.append(agent)

    for _ in range(env.player_num - 1):
        agent = RandomAgent(action_num=eval_env.action_num)
        random_agents.append(agent)

    env.set_agents(agents)
    eval_env.set_agents([agents[0], *random_agents])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):
        agents[0].train()

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            payoffs, wins = tournament(eval_env, evaluate_num)
            logger.log_performance(env.timestep, payoffs[0])
            print(f'Win rate: {(wins[0] * 100) / evaluate_num}')

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DeepCFR')

    # Save model
    save_dir = 'models/thousand_schnapsen_deep_cfr'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))
