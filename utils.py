from isolation.isolation import _WIDTH, _HEIGHT

def alpha_beta_search(state,play_id,depth=3):
    """ Return the move along a branch of the game tree that
    has the best possible value.
    """
    def min_value(state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(play_id)
        if depth <= 0:
            return score(state,play_id)
        value = float("inf")
        for action in state.actions():
            value = min(value, max_value(state.result(action), alpha, beta, depth-1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def max_value(state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(play_id)
        if depth <= 0: return score(state,play_id)
        value = float("-inf")
        for action in state.actions():
            value = max(value, min_value(state.result(action), alpha, beta, depth-1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

def wall_distance_min(state):
    own_loc = state.locs[state.ply_count % 2]
    x_player, y_player = own_loc // (_WIDTH + 2), own_loc % (_WIDTH + 2)
    return min(x_player, _WIDTH + 1 - x_player, y_player, _HEIGHT - 1 - y_player)

def score(state,play_id):
    own_loc = state.locs[play_id]
    opp_loc = state.locs[1 - play_id]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    if wall_distance_min(state) >= 2:
        return 2*len(own_liberties) - len(opp_liberties)
    else:
        return len(own_liberties) - len(opp_liberties)