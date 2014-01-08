"""
This module implements the Player (Human or AI), which is basically an
object with an ``ask_move(game)`` method
"""


class Human_Player:
    """ Class for a human player, which gets asked by text what moves
    she wants to play. She can type ``show moves`` to display a list of
    moves, or ``quit`` to quit the game.
    """
    
    def __init__(self, name = 'Human'):
        self.name = name
    
    def ask_move(self, game):
        possible_moves = map(str,game.possible_moves())
        move=-1
        while not move in possible_moves:
            move = raw_input("\nPlayer %s what do you play ? "%(
                                                      game.nplayer))
            if move == 'show moves':
                print( possible_moves )
            elif move.startswith("move #"):
                move = possible_moves[int(move[6:])]
            elif move == 'quit':
                raise KeyboardInterrupt
                
        return move

class AI_Player:
    """ Class for an AI player. This class must be initialized with an
    AI algortihm, like ``AI_Player( Negamax(9) )``
    """
    
    def __init__(self, AI_algo, name='AI'):
        self.AI_algo = AI_algo
        self.name = name
        self.move = {}
    
    def ask_move(self, game):
        return self.AI_algo(game)
