"""
This module implements transposition tables, which store positions
and moves to speed up the AI.
"""

import pickle
import json
from ast import literal_eval as make_tuple


class TT:
    """
    A tranposition table made out of a Python dictionnary.

    It creates a "cache" of already resolved moves that can, under
    some circumstances, let the algorithm run faster.

    This table can be stored to file, allowing games to be stopped
    and restarted at a later time. Or, if the game is fully solved,
    the cache can return the correct moves nearly instantly because
    the AI alogorithm no longer has to compute correct moves.

    Transposition tables can only be used on games which have a method
    game.ttentry() -> string or tuple

    To save the table as a `pickle` file, use the **tofile** and **fromfile**
    methods. A pickle file is binary and usually faster. A pickle file
    can also be appended to with new cached data. See python's pickle
    documentation for secuirty issues.

    To save the table as a universal JSON file, use the **to_json_file**
    and **from_json_file** methods. For these methods, you must explicity
    pass **use_tuples=True** if game.ttentry() returns tuples rather than
    strings.

    Usage:

        >>> table = TT()
        >>> ai = Negamax(8, scoring, tt = table)
        >>> ai(some_game) # computes a move, fills the table
        >>> table.tofile('saved_tt.data') # maybe save for later ?

        >>> # later (or in a different program)...
        >>> table = TT().fromfile('saved_tt.data')
        >>> ai = Negamax(8, scoring, tt = table)

    Transposition tables can also be used as an AI (``AI_player(tt)``)
    but they must be exhaustive in this case: if they are asked for
    a position that isn't stored in the table, it will lead to an error.

    """

    def __init__(self, own_dict=None):
        self.d = own_dict if own_dict is not None else dict()

    def lookup(self, game):
        """ Requests the entry in the table. Returns None if the
            entry has not been previously stored in the table. """
        return self.d.get(game.ttentry(), None)

    def __call__(self, game):
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

    def fromfile(self, filename):
        """ Loads a transposition table previously saved with
             ``TT.tofile`` """
        with open(filename, 'r') as h:
            self.__dict__.update(pickle.load(h).__dict__)

    def to_json_file(self, filename, use_tuples=False):
        """ Saves the transposition table to a serial JSON file. Warning: the file
            can be big (~100Mo). """
        if use_tuples:
            with open(filename, "w") as f:
                k = self.d.keys()
                v = self.d.values()
                k1 = [str(i) for i in k]
                json.dump(dict(zip(*[k1, v])), f, ensure_ascii=False)
        else:
            with open(filename, 'w') as f:
                json.dump(self.d, f, ensure_ascii=False)

    def from_json_file(self, filename, use_tuples=False):
        """ Loads a transposition table previously saved with
             ``TT.to_json_file`` """
        with open(filename, 'r') as f:
            data = f.read().decode("utf-8")
            if use_tuples:
                data = json.loads(data)
                k = data.keys()
                v = data.values()
                k1 = [make_tuple(i) for i in k]
                self.d = dict(zip(*[k1, v]))
            else:
                self.d = json.loads(data)
