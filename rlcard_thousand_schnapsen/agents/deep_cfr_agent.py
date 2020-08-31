import numpy as np
from rlcard.agents import DeepCFR as DeepCFRBase
from rlcard.agents.deep_cfr_agent import AdvantageMemory, StrategyMemory


class DeepCFR(DeepCFRBase):
    def train(self):
        """ Perform tree traversal and train the network

        Returns:
            policy_network (tf.placeholder): the trained policy network
            average advantage loss (float): players average advantage loss
        """
        # Collect samples
        init_state, _ = self._env.reset()
        for p in range(self._num_players):
            for _ in range(self._num_traversals):
                self._traverse_game_tree(init_state, p)

            for _ in range(self._num_step):
                self.advantage_losses[p] = self._learn_advantage_network(p)

        # Train policy network.
        policy_loss = 0
        for _ in range(self._num_step):
            policy_loss = self._learn_strategy_network()

        avg_adv_loss = sum(self.advantage_losses) / len(self.advantage_losses)

        self._iteration += 1

        return avg_adv_loss, policy_loss

    def _traverse_game_tree(self, state, player, count=0):
        """ Performs a traversal of the game tree.

        Over a traversal the advantage and strategy memories are populated with
        computed advantage values and matched regrets respectively.

        Args:
            state (dict): Current rlcard game state.
            player (int): Player index for this traversal.

        Returns:
            payoff (list): Recursively returns expected payoffs for each action.
        """
        actions = state['legal_actions']
        legal_actions_count = len(actions)
        current_player = self._env.get_player_id()
        if self._env.is_over():
            # Terminal state get returns.
            return self._env.get_payoffs()[player]

        if current_player == player:
            if legal_actions_count == 1:
                child_state, _ = self._env.step(actions[0])
                payoff = self._traverse_game_tree(child_state, player)
                self._env.step_back()
                return payoff

            # Update the policy over the info set & actions via regret matching.
            expected_payoff = np.zeros(self._env.action_num)
            _, strategy = self._sample_action_from_advantage(state, player)
            for action in actions:
                child_state, _ = self._env.step(action)
                expected_payoff[action] = self._traverse_game_tree(
                    child_state, player)
                self._env.step_back()
            exp_payoff_sum = strategy @ expected_payoff
            sampled_regret = expected_payoff - exp_payoff_sum
            for act in actions:
                self._advantage_memories[player].add(
                    AdvantageMemory(state['obs'], self._iteration,
                                    sampled_regret[act] / 400, act))
            return exp_payoff_sum / np.sum(strategy)
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
            exp_payoff = self._traverse_game_tree(child_state, player)
            self._env.step_back()
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
