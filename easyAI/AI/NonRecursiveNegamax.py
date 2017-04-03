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

TOP = 0
DOWN = 1
UP = 2
PRUNE = 3 # similar to UP but it prunes the remaining moves

def flipped_score(game, me, scoring):
    if game.nplayer == me:
        return scoring(game)
    return -scoring(game)

def prune_parent(state):
    index = state[CURRENT_MOVE] + 1
    state[MOVE_LIST] = state[MOVE_LIST][0:index]
    return

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

    empty_state = {
        IMAGE: None,
        MOVE_LIST: None,
        CURRENT_MOVE: None,
        BEST_MOVE: None,
        PLAYER: None,
        ALPHA: None,
        BETA: None,
    }

    states = [copy.copy(empty_state) for _ in range(target_depth + 2)]

    me = game.nplayer

    ################################################
    #
    #    START GRAND LOOP
    #
    ################################################

    depth = 0
    direction = TOP

    # if True: print "TARGET DEPTH", target_depth

    while True:
        if direction == TOP:  # this state only seen once; at the very beginning
            # if True: print "TOP",
            states[depth][IMAGE] = game.ttentry()
            states[depth][MOVE_LIST] = game.possible_moves()
            # if True: print "movelist =", states[depth][MOVE_LIST],
            states[depth][BEST_MOVE] = 0 # set default
            states[depth][BEST_SCORE] = -INF # set default
            states[depth][CURRENT_MOVE] = 0
            states[depth][PLAYER] = game.nplayer
            states[depth][ALPHA] = alpha
            states[depth][BETA] = beta
            index = states[depth][CURRENT_MOVE]
            game.make_move(states[depth][MOVE_LIST][index])
            game.switch_player()
            depth += 1
            direction = DOWN
            # if True: print "to DOWN", depth
            continue
        elif direction == DOWN:
            # if True: print "DOWN"
            # if True: print "    depth=",depth,
            if depth < target_depth and not game.is_over():  # down, down, we go...
                parent = depth - 1
                states[depth][IMAGE] = game.ttentry()
                states[depth][MOVE_LIST] = game.possible_moves()
                states[depth][BEST_MOVE] = 0 # set default
                states[depth][BEST_SCORE] = -INF # set default
                states[depth][CURRENT_MOVE] = 0
                states[depth][PLAYER] = game.nplayer
                states[depth][ALPHA] = -states[parent][BETA] # inherit alpha from -beta
                states[depth][BETA] = -states[parent][ALPHA]   # inherit beta from -alpha
                index = states[depth][CURRENT_MOVE]
                game.make_move(states[depth][MOVE_LIST][index])
                game.switch_player()
                direction = DOWN
                depth += 1
                # if True: print "    to DOWN", depth
            else: # reached a leaf or the game is over; going back up
                leaf_score = flipped_score(game, me, scoring)
                parent = depth - 1
                # if True: print "    at leaf, score=", leaf_score
                if states[parent][BEST_SCORE] < leaf_score:
                    states[parent][BEST_SCORE] = leaf_score
                    states[parent][BEST_MOVE] = states[parent][CURRENT_MOVE]
                if states[parent][ALPHA] < leaf_score:
                    states[parent][ALPHA] = leaf_score
                if states[parent][ALPHA]>=states[parent][BETA]:
                    prune_parent(states[parent])
                    # if True: print "    PRUNE!"
                direction = UP
                depth = parent
                # if True: print "    to UP", depth
            continue
        elif direction == UP:
            # if True: print "UP"
            states[depth][CURRENT_MOVE] += 1 # choose next move
            # if True: print "    depth=",depth,
            # if True: print "    new cmove=",states[depth][CURRENT_MOVE],
            # if True: print "    current movelist=",states[depth][MOVE_LIST], 
            if states[depth][CURRENT_MOVE] >= len(states[depth][MOVE_LIST]):  # out of moves
                if depth == 0:
                    break;   # we are done.
                parent = depth - 1
                best_score = states[depth][BEST_SCORE]
                if states[parent][BEST_SCORE] < best_score:
                    states[parent][BEST_SCORE] = best_score
                    states[parent][BEST_MOVE] = states[parent][CURRENT_MOVE]
                if states[parent][ALPHA] < best_score:
                    states[parent][ALPHA] = best_score
                if states[parent][ALPHA]>=states[parent][BETA]:
                    prune_parent(states[parent])
                    # if True: print "    PRUNE!"
                direction = UP
                depth = parent
                # if True: print "    to UP", depth
            else:  # with next move, go down again
                parent = depth - 1
                game.ttrestore(states[depth][IMAGE])
                game.nplayer = states[depth][PLAYER]
                index = states[depth][CURRENT_MOVE]
                game.make_move(states[depth][MOVE_LIST][index])
                game.switch_player()
                direction = DOWN
                depth += 1
                # if True: print "    to DOWN", depth

    best_move_index = states[0][BEST_MOVE]
    best_move = states[0][MOVE_LIST][best_move_index]
    best_value = states[0][BEST_SCORE]
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
