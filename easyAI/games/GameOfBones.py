""" This is the example featured in section 'A quick example' of the docs """

from easyAI import TwoPlayersGame


class GameOfBones(TwoPlayersGame):
    """ In turn, the players remove one, two or three bones from a
    pile of bones. The player who removes the last bone loses. """

    def __init__(self, players):
        self.players = players
        self.pile = 20 # start with 20 bones in the pile
        self.nplayer = 1 # player 1 starts

    def possible_moves(self): return ['1', '2', '3']

    def make_move(self, move): self.pile -= int(move) # remove bones.

    def win(self): return self.pile <= 0 # opponent took the last bone ?

    def is_over(self): return self.win() # game stops when someone wins.

    def scoring(self): return 100 if self.win() else 0

    def show(self): print("%d bones left in the pile" % (self.pile))


if __name__ == "__main__":
    """
    Start a match (and store the history of moves when it ends)
    ai = Negamax(10) # The AI will think 10 moves in advance 
    game = GameOfBones( [ AI_Player(ai), Human_Player() ] )
    history = game.play()
    """

    # Let's solve the game

    from easyAI import id_solve, Human_Player, AI_Player
    from easyAI.AI import TT

    tt = TT()
    GameOfBones.ttentry = lambda self: self.pile
    r, d, m = id_solve(GameOfBones, range(2, 20), win_score = 100, tt = tt)
    print(r, d, m)  # see the docs.

    # Unbeatable AI !

    game = GameOfBones([AI_Player(tt), Human_Player()])
    game.play() # you will always lose this game :)
