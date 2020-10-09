"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
Turn=X

EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    Xcounter = 0
    Ocounter = 0
    for row in board:
        Xcounter += row.count(X)
        Ocounter += row.count(O)

    if Xcounter == Ocounter:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    posMoves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                posMoves.append([i, j])
    return posMoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board2= copy.deepcopy(board)
    try:
        if board2[action[0]][action[1]] != EMPTY:
            raise IndexError
        else:
            board2[action[0]][action[1]] = player(board2)
            return board2
    except IndexError:
        print('Busy space')


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    column=[]
    #review rows winner
    for r in board:
        Xcounter = r.count(X)
        Ocounter = r.count(O)
        if Xcounter == 3:
            return X
        if Ocounter == 3:
            return O
    #Review columns
    for i in range (len(board)):
        c=[row[i] for row in board]
        column.append(c)
    for i in column:
        Xcounter = i.count(X)
        Ocounter = i.count(O)
        if Xcounter ==3:
            return X
        if Ocounter ==3:
            return O
    #Diagonal winner
    if board[0][0]== O and board[1][1] == O and board [2][2]==O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    #if no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    counter=0
    for r in board:
        counter += r.count(EMPTY)
    if counter == 0:
        return True
    elif winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_move=""
    #Know the current player
    current_player = player(board)
    #If palyer is X
    if current_player == X:

        v = -math.inf
        for action in actions(board):
            k = min_value(result(board, action))   
            if k > v:
                v = k
                best_move = action
    else:
        v = math.inf
        for action in actions(board):
            k = max_value(result(board, action))    
            if k < v:
                v = k
                best_move = action
    return best_move

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v    

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v    
