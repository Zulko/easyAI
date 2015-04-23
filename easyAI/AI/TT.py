"""
This module implements transposition tables, which store positions
and moves to speed up the AI.
"""

import pickle
from easyAI.AI.DictTT import DictTT

class TT:
    """
    A tranposition table made out of a Python dictionnary.
    It can only be used on games which have a method
    game.ttentry() -> string, or tuple
    
    Usage:
        
        >>> table = TT(DictTT(1024)) or table = TT() for default dictionary
        >>> ai = Negamax(8, scoring, tt = table) # boosted Negamax !
        >>> ai(some_game) # computes a move, fills the table
        >>> table.to_file('saved_tt.data') # maybe save for later ?
        
        >>> # later...
        >>> table = TT.fromfile('saved_tt.data')
        >>> ai = Negamax(8, scoring, tt = table) # boosted Negamax !
    
    Transposition tables can also be used as an AI (``AI_player(tt)``)
    but they must be exhaustive in this case: if they are asked for
    a position that isn't stored in the table, it will lead to an error.
    
    """
    
    def __init__(self, own_dict = None):
        self.d = own_dict if own_dict != None else dict()
        
    def lookup(self, game):
        """ Requests the entry in the table. Returns None if the
            entry has not been previously stored in the table. """
        return self.d.get(game.ttentry(), None)
        
    def __call__(self,game):
        """
        This method enables the transposition table to be used
        like an AI algorithm. However it will just break if it falls
        on some game state that is not in the table. Therefore it is a
        better option to use a mixed algorithm like
        
        >>> # negamax boosted with a transposition table !
        >>> Negamax(10, tt= my_dictTT) 
        """
        return self.d[game.ttentry()]['move']
        
    def store(self, **data):
        """ Stores an entry into the table """        
        entry = data.pop("game").ttentry()
        self.d[entry] = data
        
    def tofile(self, filename):
        """ Saves the transposition table to a file. Warning: the file
            can be big (~100Mo). """
        with open(filename, 'w+') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def fromfile(self, filename):
        """ Loads a transposition table previously saved with
             ``TT.tofile`` """
        with open(filename, 'r') as f:
            pickle.load(self, filename)
