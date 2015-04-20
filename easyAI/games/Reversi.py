"""
The game of Reversi. Warning: this game is not coded in an optimal
way, the AI will be slow.
"""

import numpy as np
from easyAI import TwoPlayersGame

to_string = lambda a : "ABCDEFGH"[a[0]] + str(a[1]+1)
to_array = lambda s : np.array(["ABCDEFGH".index(s[0]),int(s[1])-1])

class Reversi( TwoPlayersGame ):
    """
    See the rules on http://en.wikipedia.org/wiki/Reversi
    Here for simplicity we suppose that the game ends when a
    player cannot play, but it would take just a few more lines to
    implement the real ending rules, by which the game ends when both
    players can't play.
    
    This implementation will make a slow and dumbe AI and could be sped
    up by adding a way of unmaking moves (method unmake_moves) and
    coding some parts in C (this is left as an exercise :) )
    """

    def __init__(self, players, board = None):
        self.players = players
        self.board = np.zeros((8,8), dtype=int)
        self.board[3,[3,4]] = [1,2]
        self.board[4,[3,4]] = [2,1]
        self.nplayer=1


    def possible_moves(self):
        """ Only moves that lead to flipped pieces are allowed """
        return [to_string((i,j)) for i in range(8) for j in range(8)
            if (self.board[i,j] == 0)
            and (pieces_flipped(self.board, (i,j), self.nplayer) != [])]

    def make_move(self, pos):
        """ Put the piece at position ``pos`` and flip the pieces that
        much be flipped """
        pos= to_array(pos)
        flipped = pieces_flipped(self.board, pos, self.nplayer)
        for i,j in flipped:
            self.board[i,j] = self.nplayer
        self.board[pos[0],pos[1]] = self.nplayer

    def show(self):
        """ Prints the board in a fancy (?) way """
        print('\n'+'\n'.join(['  1 2 3 4 5 6 7 8']+ ['ABCDEFGH'[k] +
                ' '+' '.join([['.','1','2','X'][self.board[k][i]]
                for i in range(8)]) for k in range(8)]+['']))

    def is_over(self):
        """ The game is considered over when someone cannot play. That
        may not be the actual rule but it is simpler to code :). Of
        course it would be possible to implement that a player can pass
        if it cannot play (by adding the move 'pass')"""
        return self.possible_moves() == []

    def scoring(self):
        """
        In the beginning of the game (less than 32 pieces) much
        importance is given to placing pieces on the border. After this
        point, only the number of pieces of each player counts
        """

        if np.sum(self.board==0) > 32: # less than half the board is full
            player = self.board==self.nplayer
            opponent = self.board==self.nopponent
            return ((player-opponent)*BOARD_SCORE).sum()
        else:
            npieces_player = np.sum(self.board==self.nplayer)
            npieces_opponent = np.sum(self.board==self.nopponent)
            return  npieces_player - npieces_opponent

# This board is used by the AI to give more importance to the border
BOARD_SCORE = np.array( [[9,3,3,3,3,3,3,9],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [3,1,1,1,1,1,1,3],
                         [9,3,3,3,3,3,3,9]])

DIRECTIONS = [ np.array([i,j]) for i in [-1,0,1] for j in [-1,0,1]
                               if (i!=0 or j!=0)]

def pieces_flipped(board, pos, nplayer):
    """
    Returns a list of the positions of the pieces to be flipped if
    player `nplayer` places a piece on the `board` at position `pos`.
    This is slow and could be coded in C or Cython.
    """

    flipped = []

    for d in DIRECTIONS:
        ppos = pos + d
        streak = []
        while (0<=ppos[0]<=7) and (0<=ppos[1]<=7):
            if board[ppos[0],ppos[1]] == 3 - nplayer:
                streak.append(+ppos)
            elif board[ppos[0],ppos[1]] == nplayer:
                flipped += streak
                break
            else:
                break
            ppos += d

    return flipped

if __name__ == "__main__":
    from easyAI import Human_Player, AI_Player, Negamax

    # An example: Computer vs Computer:
    game = Reversi([AI_Player(Negamax(4)), AI_Player(Negamax(4))])
    game.play()
    if game.scoring() > 0:
        print("player %d wins." % game.nplayer)
    elif game.scoring() < 0:
        print("player %d wins." % game.nopponent)
    else:
        print("Draw.")
