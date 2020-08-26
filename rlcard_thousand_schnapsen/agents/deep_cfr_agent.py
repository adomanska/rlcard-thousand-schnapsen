import numpy as np
from rlcard.agents import DeepCFR as DeepCFRBase
from rlcard.agents.deep_cfr_agent import AdvantageMemory, StrategyMemory


class DeepCFR(DeepCFRBase):
    def train(self):
        """ Perform tree traversal and train the network

        Returns:
            policy_network (tf.placeholder): the trained policy network
            average advantage loss (float): players average advantage loss
            policy loss (float): policy loss
        """
        init_state, _ = self._env.reset()
        for p in range(self._num_players):
            for _ in range(self._num_traversals):
                self._traverse_game_tree(init_state, p)

            # Re-initialize advantage networks and train from scratch.
            self.reinitialize_advantage_networks()
            for _ in range(self._num_step):
                self.advantage_losses[p] = self._learn_advantage_network(p)

            # Re-initialize advantage networks and train from scratch.
            self._iteration += 1

        # Train policy network.
        for _ in range(self._num_step):
            policy_loss = self._learn_strategy_network()

        avg_adv_loss = sum(self.advantage_losses) / len(self.advantage_losses)

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
        current_player = self._env.get_player_id()
        if self._env.is_over():
            # Terminal state get returns.
            self.traverse = []
            return self._env.get_payoffs()[player]

        if current_player == player:
            # Update the policy over the info set & actions via regret matching.
            expected_payoff = np.zeros(self._env.action_num)
            _, strategy = self._sample_action_from_advantage(state, player)
            for action in actions:
                child_state, _ = self._env.step(action)
                self.traverse.append((action, state, child_state))
                expected_payoff[action] = self._traverse_game_tree(
                    child_state, player)
                self._env.step_back()
            sampled_regret = expected_payoff - np.sum(
                strategy * expected_payoff)
            for act in actions:
                self._advantage_memories[player].add(
                    AdvantageMemory(state['obs'].flatten(), self._iteration,
                                    sampled_regret[act], act))
            return max(expected_payoff)
        else:
            other_player = current_player
            _, strategy = self._sample_action_from_advantage(
                state, other_player)
            # Recompute distribution dor numerical errors.
            probs = np.array(strategy)
            probs /= probs.sum()
            action = np.random.choice(range(self._num_actions), p=probs)
            child_state, _ = self._env.step(action)
            self._strategy_memories.add(
                StrategyMemory(state['obs'].flatten(), self._iteration,
                               strategy))
            exp_payoff = self._traverse_game_tree(child_state, player)
            self._env.step_back()
            return exp_payoff
