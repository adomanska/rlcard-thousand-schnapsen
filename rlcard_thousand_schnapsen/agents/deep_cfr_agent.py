import numpy as np
from rlcard.agents import DeepCFR as DeepCFRBase
from rlcard.agents.deep_cfr_agent import AdvantageMemory, StrategyMemory, FixedSizeRingBuffer
import tensorflow as tf


class DeepCFR(DeepCFRBase):
    def __init__(self,
                 session,
                 scope,
                 env,
                 policy_network_layers=(32, 32),
                 advantage_network_layers=(32, 32),
                 num_traversals=10,
                 num_step=40,
                 learning_rate=1e-4,
                 batch_size_advantage=16,
                 batch_size_strategy=16,
                 memory_capacity=int(1e7),
                 strategy_memory_capacity: int = None):
        super().__init__(session, scope, env, policy_network_layers,
                         advantage_network_layers, num_traversals, num_step,
                         learning_rate, batch_size_advantage,
                         batch_size_strategy, memory_capacity)
        if strategy_memory_capacity is not None:
            self._strategy_memories = FixedSizeRingBuffer(
                strategy_memory_capacity)

    def train(self):
        """ Perform tree traversal and train the network

        Returns:
            policy_network (tf.placeholder): the trained policy network
            average advantage loss (float): players average advantage loss
        """
        # Collect samples
        init_state, _ = self._env.reset()
        for p in range(self._num_players):
            cache = {}
            cache_size = 0
            while True: 
                self._traverse_game_tree(init_state, p, cache)
                if len(cache) == cache_size:
                    break
                cache_size = len(cache)
            print(len(cache))

            self.reinitialize_advantage_network(p)
            for _ in range(self._num_step):
                self.advantage_losses[p] = self._learn_advantage_network(p)

        # Train policy network.
        self.reinitialize_policy_network()
        policy_loss = 0
        for _ in range(self._num_step):
            policy_loss = self._learn_strategy_network()

        avg_adv_loss = sum(self.advantage_losses) / len(self.advantage_losses)

        self._iteration += 1

        return avg_adv_loss, policy_loss

    @staticmethod
    def reinitialize_advantage_network(player_id: int):
        """ Reinitialize the advantage network
        """
        advantage_vars = [
            v for v in tf.global_variables()
            if f'{player_id}_advantage' in v.name
        ]
        tf.variables_initializer(var_list=advantage_vars)

    @staticmethod
    def reinitialize_policy_network():
        """ Reinitialize the policy network
        """
        policy_vars = [
            v for v in tf.global_variables() if 'advantage' not in v.name
        ]
        tf.variables_initializer(var_list=policy_vars)

    def _traverse_game_tree(self, state, player, cache = {}, points = 0):
        """ Performs a traversal of the game tree.

        Over a traversal the advantage and strategy memories are populated with
        computed advantage values and matched regrets respectively.

        Args:
            state (dict): Current rlcard game state.
            player (int): Player index for this traversal.

        Returns:
            payoff (list): Recursively returns expected payoffs for each action.
        """
        state_hash = state['hash']

        if state_hash in cache:
            return points + cache[state_hash]
        
        actions = state['legal_actions']
        legal_actions_count = len(actions)
        current_player = self._env.get_player_id()
        if self._env.is_over():
            # Terminal state get returns.
            return self._env.get_payoffs()[player]

        if current_player == player:
            if legal_actions_count == 1:
                child_state, _ = self._env.step(actions[0])
                new_points = self._env.get_reward(player)
                payoff = self._traverse_game_tree(child_state, player, cache, new_points)
                self._env.step_back()
                cache[state_hash] = payoff - points
                return payoff

            # Update the policy over the info set & actions via regret matching.
            expected_payoff = np.zeros(self._env.action_num)
            _, strategy = self._sample_action_from_advantage(state, player)
            for action in actions:
                child_state, _ = self._env.step(action)
                new_points = self._env.get_reward(player)
                expected_payoff[action] = self._traverse_game_tree(
                    child_state, player, cache, new_points)
                self._env.step_back()
            exp_payoff_sum = strategy @ expected_payoff
            sampled_regret = expected_payoff - exp_payoff_sum
            for act in actions:
                self._advantage_memories[player].add(
                    AdvantageMemory(state['obs'], self._iteration,
                                    sampled_regret[act] / 400, act))
            payoff = exp_payoff_sum / np.sum(strategy)
            cache[state_hash] = payoff - points
            return payoff
        else:
            other_player = current_player
            if legal_actions_count == 1:
                action = actions[0]
            else:
                _, strategy = self._sample_action_from_advantage(
                    state, other_player)
                action = np.random.choice(range(self._num_actions), p=strategy)
                self._strategy_memories.add(
                    StrategyMemory(state['obs'], self._iteration, strategy))
            child_state, _ = self._env.step(action)
            new_points = self._env.get_reward(player)
            exp_payoff = self._traverse_game_tree(child_state, player, cache, new_points)
            self._env.step_back()
            cache[state_hash] = exp_payoff - points
            return exp_payoff

    def _sample_action_from_advantage(self, state, player):
        """ Returns an info state policy by applying regret-matching.

        Args:
            state (dict): Current state.
            player (int): Player index over which to compute regrets.

        Returns:
            1. (list) Advantage values for info state actions indexed by action.
            2. (list) Matched regrets, prob for actions indexed by action.
        """
        info_state = state['obs']
        legal_actions = state['legal_actions']
        advantages = self._session.run(self._advantage_outputs[player],
                                       feed_dict={
                                           self._info_state_ph:
                                           np.expand_dims(info_state, axis=0)
                                       })[0]
        advantages = np.clip(advantages, 0, None)
        cumulative_regret = np.sum(advantages[legal_actions])
        matched_regrets = np.zeros(self._num_actions)
        if cumulative_regret > 0. and self._iteration > 1:
            matched_regrets[
                legal_actions] = advantages[legal_actions] / cumulative_regret
        else:
            matched_regrets[legal_actions] = 1. / len(legal_actions)
        matched_regrets /= np.sum(matched_regrets)
        return advantages, matched_regrets
