import numpy as np
from easyAI import TwoPlayersGame


# directions in which a knight can move
DIRECTIONS = list(map(np.array, [[1, 2], [-1, 2], [1, -2], [-1, -2],
                            [2, 1], [2, -1], [-2, 1], [-2, -1]]))

# functions to convert "D8" into (3,7) and back...
pos2string = lambda ab: "ABCDEFGH"[ab[0]] + str(ab[1] + 1)
string2pos = lambda s: np.array(["ABCDEFGH".index(s[0]), int(s[1])-1])


class Knights(TwoPlayersGame):
    """
    Each player has a chess knight (that moves in "L") on a chessboard.
    Each turn the player moves the knight to any tile that hasn't been
    occupied by a knight before. The first player that cannot move loses.
    """

    def __init__(self, players, board_size = (8, 8)):
        self.players = players
        self.board_size = board_size
        self.board = np.zeros(board_size, dtype = int)
        self.board[0, 0] = 1
        self.board[board_size[0] - 1, board_size[1] - 1] = 2
        players[0].pos = np.array([0, 0])
        players[1].pos = np.array([board_size[0] - 1, board_size[1]-1])
        self.nplayer = 1 # player 1 starts.

    def possible_moves(self):
        endings = [self.player.pos + d for d in DIRECTIONS]
        return [pos2string(e) for e in endings # all positions
                if (e[0] >= 0) and (e[1] >= 0) and
                   (e[0] < self.board_size[0]) and
                   (e[1] < self.board_size[1]) and # inside the board
                   self.board[e[0], e[1]] == 0] # and not blocked

    def make_move(self, pos):
        pi, pj = self.player.pos
        self.board[pi, pj] = 3 # 3 means blocked
        self.player.pos = string2pos(pos)
        pi, pj = self.player.pos
        self.board[pi, pj] = self.nplayer # place player on board

    def ttentry(self):
        e = [tuple(row) for row in self.board]
        e.append(pos2string(self.players[0].pos))
        e.append(pos2string(self.players[1].pos))
        return tuple(e)

    def ttrestore(self, entry):
        for x, row in enumerate(entry[:self.board_size[0]]):
            for y, n in enumerate(row):
                self.board[x, y] = n
        self.players[0].pos = string2pos(entry[-2])
        self.players[1].pos = string2pos(entry[-1])

    def show(self):
        print('\n' + '\n'.join(['  1 2 3 4 5 6 7 8'] +
              ['ABCDEFGH'[k] + 
               ' ' + ' '.join([['.', '1', '2', 'X'][self.board[k, i]]
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

    ai_algo = Negamax(11)
    game = Knights([AI_Player(ai_algo), AI_Player(ai_algo)], (5, 5))
    game.play()
    print("player %d loses" % (game.nplayer))
