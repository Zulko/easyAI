"""
The standard AI algorithm of easyAI is Negamax with alpha-beta pruning.
This version does not use recursion. It also does not support transposition
tables, but it does REQUIRE the `tt_entry` method in the game.

It does not make use of 'unmake_move', though having it will not cause a
problem.

It also requires a reverse function: 'tt_restore' that takes the value from
'tt_entry' and restores the game state.
"""

import copy

LOWERBOUND, EXACT, UPPERBOUND = -1, 0, 1

INF = float('infinity')

# integer keys for 'state':
IMAGE = 0
MOVE_LIST = 1
CURRENT_MOVE = 2
BEST_MOVE = 3
BEST_SCORE = 4
PLAYER = 5
ALPHA = 6
BETA = 7

DOWN = 1
UP = 2

class StateObject(object):

    def __init__(self):
        self.image = None
        self.move_list = []
        self.current_move = 0
        self.best_move = 0
        self.best_score = -INF
        self.player = None
        self.alpha = -INF
        self.beta = INF

    def prune(self):
        index = self.current_move + 1
        self.move_list = self.move_list[0:index]

    def out_of_moves(self):
        ''' we are at or past the end of the move list '''
        return self.current_move >= len(self.move_list) - 1

    def goto_next_move(self):
        self.current_move += 1
        return self.move_list[self.current_move]

    def swap_alpha_beta(self):
        (self.alpha, self.beta) = (self.beta, self.alpha)


class StateList(object):


    def __init__(self, target_depth):
        self.state_list = [StateObject() for _ in range(target_depth + 2)]

    def __getitem__(self, key):
        return self.state_list[key + 1]


def negamax_nr(game, target_depth, scoring, alpha=-INF, beta=+INF):

    ################################################
    #
    #    INITIALIZE AND CHECK ENTRY CONDITIONS
    #
    ################################################

    if not hasattr(game, "ttentry"):
        raise AttributeError('Method "ttentry()" missing from game.')
    if not hasattr(game, "ttrestore"):
        raise AttributeError('Method "ttrestore()" missing from game.')

    if (target_depth == 0) or game.is_over():
        score = scoring(game)
        game.ai_move = None
        return score


    states = StateList(target_depth)

    me = game.nplayer

    ################################################
    #
    #    START GRAND LOOP
    #
    ################################################

    depth = -1  # proto-parent
    states[depth].alpha = alpha
    states[depth].beta = beta
    direction = DOWN
    depth = 0

    while True:
        # print "DEPTH", target_depth - depth
        parent = depth - 1
        if direction == DOWN:
            if (depth < target_depth) and not game.is_over():  # down, down, we go...
                states[depth].image = game.ttentry()
                states[depth].move_list = game.possible_moves()
                # print "MOVES", states[depth].move_list
                states[depth].best_move = 0
                states[depth].best_score = -INF
                states[depth].current_move = 0
                states[depth].player = game.nplayer
                states[depth].alpha = -states[parent].beta # inherit alpha from -beta
                states[depth].beta = -states[parent].alpha   # inherit beta from -alpha
                index = states[depth].current_move
                game.make_move(states[depth].move_list[index])
                game.switch_player()
                direction = DOWN
                depth += 1
            else: # reached a leaf or the game is over; going back up
                leaf_score = -scoring(game)
                # print "LEAF w AB", -leaf_score, -states[parent].beta, -states[parent].alpha
                if leaf_score > states[parent].best_score:
                    states[parent].best_score = leaf_score
                    states[parent].best_move = states[parent].current_move
                # print "BEST_SCORE SO FAR", states[parent].best_score, "at", (target_depth - parent)
                if states[parent].alpha < leaf_score:
                    # print "LEAF CHANGE ALPHA to ", leaf_score, "for", (target_depth - parent)
                    states[parent].alpha = leaf_score
                direction = UP
                depth = parent
            continue
        elif direction == UP:
            prune_time = states[depth].alpha >= states[depth].beta
            if states[depth].out_of_moves() or prune_time:  # out of moves
                bs = -states[depth].best_score
                if bs > states[parent].best_score:
                    states[parent].best_score = bs
                    states[parent].best_move = states[parent].current_move
                if states[parent].alpha < bs:
                    # print "UP CHANGE ALPHA to ", bs, "for", (target_depth - parent)
                    states[parent].alpha = bs
                # print "UP BEST_SCORE SO FAR", bs, states[parent].move_list[states[parent].best_move], "to", (target_depth - parent)
                # print "BEST_SCORE, BEST_MOVE", bs, states[depth].move_list[states[depth].best_move], "at", (target_depth - depth)
                if depth<=0:
                    break   # we are done.
                direction = UP
                depth = parent
                #if prune_time:
                    # print "PRUNE (via UP)"
                continue
            # else go down the next branch
            game.ttrestore(states[depth].image)
            game.nplayer = states[depth].player
            next_move = states[depth].goto_next_move()
            game.make_move(next_move)
            game.switch_player()
            direction = DOWN
            depth += 1

    best_move_index = states[0].best_move
    best_move = states[0].move_list[best_move_index]
    best_value = states[0].best_score
    game.ai_move = best_move
    return best_value


class NonRecursiveNegamax:
    """
    This implements Negamax without recursion. The following example shows
    how to setup the AI and play a Connect Four game:
    
        >>> from easyAI.games import ConnectFour
        >>> from easyAI import NonRecursiveNegamax, Human_Player, AI_Player
        >>> scoring = lambda game: -100 if game.lose() else 0
        >>> ai_algo = NonRecursiveNegamax(8, scoring) # AI will think 8 turns in advance
        >>> game = ConnectFour([Human_Player(), AI_Player(ai_algo)])
        >>> game.play()
    
    Parameters
    -----------
    
    depth:
      How many moves in advance should the AI think ?
      (2 moves = 1 complete turn)
    
    scoring:
      A function f(game)-> score. If no scoring is provided
         and the game object has a ``scoring`` method it ill be used.
    
    win_score:
      Score above which the score means a win. This will be
        used to speed up computations if provided, but the AI will not
        differentiate quick defeats from long-fought ones (see next
        section).
        
    tt:
      A transposition table (a table storing game states and moves)
      scoring: can be none if the game that the AI will be given has a
      ``scoring`` method.
      
    Notes
    -----
   
    The score of a given game is given by
    
    >>> scoring(current_game) - 0.01*sign*current_depth
    
    for instance if a lose is -100 points, then losing after 4 moves
    will score -99.96 points but losing after 8 moves will be -99.92
    points. Thus, the AI will chose the move that leads to defeat in
    8 turns, which makes it more difficult for the (human) opponent.
    This will not always work if a ``win_score`` argument is provided.
    
    """

    def __init__(self, depth, scoring=None, win_score=+INF, tt=None):
        self.scoring = scoring        
        self.depth = depth
        self.tt = tt
        self.win_score = win_score

    def __call__(self, game):
        """
        Returns the AI's best move given the current state of the game.
        """
        scoring = self.scoring if self.scoring else (
            lambda g: g.scoring() 
        )
        temp = game.copy()
        self.alpha = negamax_nr(
            temp,
            self.depth,
            scoring,
            -self.win_score,
            +self.win_score
        )
        return temp.ai_move
