import random, math, copy

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.children_actions = []
        self.parent = parent

    def add_child(self, child_state, action):
        child = MonteCarloTreeSearchNode(child_state, self)
        self.children.append(child)
        self.children_actions.append(action)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        return len(self.children_actions) == len(self.state.actions())
    
factor = 1.0
iterations_limit = 90

def explore(node):
    while not node.state.terminal_test():
        if not node.fully_explored():
            return expand(node)
        node = best_child(node)
    return node

def expand(node):
    tried_actions = node.children_actions
    legal_actions = node.state.actions()
    for action in legal_actions:
        if action not in tried_actions:
            new_state = node.state.result(action)
            node.add_child(new_state, action)
            return node.children[-1]
        
def best_child(node):
    best_score = float("-inf")
    best_children = []
    for child in node.children:
        exploit = child.reward / child.visits
        explore = math.sqrt(2.0 * math.log(node.visits) / child.visits)
        score = exploit + factor * explore
        if score == best_score:
            best_children.append(child)
        elif score > best_score:
            best_children = [child]
            best_score = score
    return random.choice(best_children)

def random_child(state):
    init_state = copy.deepcopy(state)
    while not state.terminal_test():
        action = random.choice(state.actions())
        state = state.result(action)
    return -1 if state._has_liberties(init_state.player()) else 1

def backpropagate(node, reward):
    while node != None:
        node.update(reward)
        node = node.parent
        reward *= -1