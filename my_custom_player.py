
from sample_players import DataPlayer
from monte_carlo_search import *
from utils import *
import random

class MinimaxPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        """import random
        self.queue.put(random.choice(state.actions()))
        """
        if state.ply_count < 4:
            if state in self.data:
                self.queue.put(self.data[state])
            else:
                self.queue.put(random.choice(state.actions()))
        else:
            depth_limit = 50
            for depth in range(1, depth_limit + 1):
                best_move = alpha_beta_search(state, self.player_id, depth)
            self.queue.put(best_move)

class MonteCarloPlayer(DataPlayer):
    
    def monte_carlo_tree_search(self, state):
        root = MonteCarloTreeSearchNode(state)
        if root.state.terminal_test():
            return random.choice(state.actions())
        for _ in range(iterations_limit):
            child = explore(root)
            if not child:
                continue
            reward = random_child(child.state)
            backpropagate(child, reward)
        idx = root.children.index(best_child(root))
        return root.children_actions[idx]
    
    def get_action(self, state):
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.monte_carlo_tree_search(state))

"""CustomPlayer = MinimaxPlayer"""
CustomPlayer = MonteCarloPlayer
