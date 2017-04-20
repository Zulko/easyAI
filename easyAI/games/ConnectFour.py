try:
    import numpy as np
except ImportError:
    print("Sorry, this example requires Numpy installed !")
    raise

from easyAI import TwoPlayersGame


class ConnectFour(TwoPlayersGame):
    """
    The game of Connect Four, as described here:
    http://en.wikipedia.org/wiki/Connect_Four
    """

    def __init__(self, players, board = None):
        self.players = players
        self.board = board if (board != None) else (
            np.array([[0 for i in range(7)] for j in range(6)]))
        self.nplayer = 1 # player 1 starts.

    def possible_moves(self):
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.nplayer

    def show(self):
        print('\n' + '\n'.join(
                        ['0 1 2 3 4 5 6', 13 * '-'] +
                        [' '.join([['.', 'O', 'X'][self.board[5 - j][i]]
                        for i in range(7)]) for j in range(6)]))

    def lose(self):
        return find_four(self.board, self.nopponent)

    def is_over(self):
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0


def find_four(board, nplayer):
    """
    Returns True iff the player has connected  4 (or more)
    This is much faster if written in C or Cython
    """
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == nplayer:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False


POS_DIR = np.array([[[i, 0], [0, 1]] for i in range(6)] +
                   [[[0, i], [1, 0]] for i in range(7)] +
                   [[[i, 0], [1, 1]] for i in range(1, 3)] +
                   [[[0, i], [1, 1]] for i in range(4)] +
                   [[[i, 6], [1, -1]] for i in range(1, 3)] +
                   [[[0, i], [1, -1]] for i in range(3, 7)])

if __name__ == '__main__':
    # LET'S PLAY !

    from easyAI import Human_Player, AI_Player, Negamax, SSS, DUAL

    ai_algo_neg = Negamax(5)
    ai_algo_sss = SSS(5)
    game = ConnectFour([AI_Player(ai_algo_neg), AI_Player(ai_algo_sss)])
    game.play()
    if game.lose():
        print("Player %d wins." % (game.nopponent))
    else:
        print("Looks like we have a draw.")
