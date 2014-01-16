import numpy as np
from easyAI import TwoPlayersGame


# directions in which a knight can move
DIRECTIONS = list(map(np.array, [[1, 2], [-1, 2], [1, -2], [-1, -2],
                                 [2, 1], [2, -1], [-2, 1], [-2, -1]]))


# functions to convert "D8" into (3,7) and back...
pos2string = lambda a: "ABCDEFGH"[a[0]] + str(a[1] + 1)
string2pos = lambda s: ["ABCDEFGH".index(s[0]), int(s[1]) - 1]

mov2string = lambda m: pos2string((m[0], m[1])) + " " + pos2string((m[2], m[3]))


def string2mov(s):
    poss = [string2pos(p) for p in s.split(" ")]
    return poss[0] + poss[1]


class Cram(TwoPlayersGame):
    """
    Players place a domino on the grid (provide x1,y1,x2,y2)
    """

    def __init__(self, players, board_size = (6, 6)):
        self.players = players
        self.board_size = board_size
        self.board = np.zeros(board_size, dtype = int)
        self.nplayer = 1 # player 1 starts.

    def possible_moves(self):
        moves = []
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                if self.board[i, j] == 0:
                    if (i + 1) < self.board_size[0] and self.board[i + 1, j] == 0:
                        moves.append([i, j, i + 1, j])
                    if (j + 1) < self.board_size[1] and self.board[i, j + 1] == 0:
                        moves.append([i, j, i, j + 1])
        return list(map(mov2string, moves))

    def make_move(self, move):
        move = string2mov(move)
        self.board[move[0], move[1]] = 1
        self.board[move[2], move[3]] = 1

    def unmake_move(self, move):
        move = string2mov(move)
        self.board[move[0], move[1]] = 0
        self.board[move[2], move[3]] = 0

    def show(self):
        print('\n' + '\n'.join(['  1 2 3 4 5 6 7 8'] + ['ABCDEFGH'[k] +
                                                        ' ' + ' '.join(['.*'[self.board[k, i]]
                                                        for i in range(self.board_size[0])])
                                                        for k in range(self.board_size[1])] + ['']))

    def lose(self):
        return self.possible_moves() == []

    def scoring(self):
        return -100 if (self.possible_moves() == []) else 0

    def is_over(self):
        return self.lose()


if __name__ == "__main__":
    from easyAI import AI_Player, Negamax

    ai_algo = Negamax(6)
    game = Cram([AI_Player(ai_algo), AI_Player(ai_algo)], (5, 5))
    game.play()
    print("player {%d} loses".format(game.nplayer))