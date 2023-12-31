"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = sum([row.count(X) for row in board])
    O_count = sum([row.count(O) for row in board])
    EMPTY_count = sum([row.count(EMPTY) for row in board])

    if EMPTY_count == 9:
        return X
    elif X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (i, j) = action
    new_board = copy.deepcopy(board)
    try:
        if new_board[i][j] != EMPTY:
            raise Exception
        else:
            new_board[i][j] = player(new_board)
            return new_board
    except:
        raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Row Victory
    for row in board:
        X_count = row.count(X)
        if X_count == 3:
            return X

        O_count = row.count(O)
        if O_count == 3:
            return O

    # Diagonal Victory
    diagonals = [board[i][i] for i in range(3)]
    X_count = diagonals.count(X)
    if X_count == 3:
        return X

    O_count = diagonals.count(O)
    if O_count == 3:
        return O

    # Off-diagonal Victory
    off_diagonals = [board[i][2 - i] for i in range(3)]
    X_count = off_diagonals.count(X)
    if X_count == 3:
        return X

    O_count = off_diagonals.count(O)
    if O_count == 3:
        return O

    # Column Victory
    for j in range(3):
        column = []
        for i in range(3):
            column.append(board[i][j])

        X_count = column.count(X)
        if X_count == 3:
            return X

        O_count = column.count(O)
        if O_count == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner_symbol = winner(board)
    if winner_symbol:
        return True
    else:
        EMPTY_count = sum([row.count(EMPTY) for row in board])
        return EMPTY_count == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_symbol = winner(board)
    if winner_symbol == X:
        return 1
    elif winner_symbol == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        player_symbol = player(board)
        actions_set = actions(board)
        actions_dict = dict()
        if player_symbol == X:
            pruned_value = -math.inf
            for action in actions_set:
                actions_dict[action] = minimizer(result(board, action), pruned_value)
                pruned_value = max(pruned_value, actions_dict[action])
            best_pair = sorted(actions_dict.items(), key=lambda x: x[1], reverse=True)
            return best_pair[0][0]
        else:
            pruned_value = math.inf
            for action in actions_set:
                actions_dict[action] = maximizer(result(board, action), pruned_value)
                pruned_value = min(pruned_value, actions_dict[action])
            best_pair = sorted(actions_dict.items(), key=lambda x: x[1])
            return best_pair[0][0]


def maximizer(board, pruned_value):
    if terminal(board):
        return utility(board)

    actions_set = actions(board)
    value = -math.inf
    for action in actions_set:
        value = max(value, minimizer(result(board, action), value))
        if value > pruned_value:
            return value
    return value


def minimizer(board, pruned_value):
    if terminal(board):
        return utility(board)

    actions_set = actions(board)
    value = math.inf
    for action in actions_set:
        value = min(value, maximizer(result(board, action), value))
        if value < pruned_value:
            return value
    return value
