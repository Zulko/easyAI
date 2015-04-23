from easyAI.AI import Negamax
from easyAI.AI import TT
from easyAI.Player import AI_Player

def id_solve(game, ai_depths, win_score, scoring=None,
          tt=None, verbose=True):
    """
    Solves a game using iterative deepening, i.e. determines if by playing
    perfectly the first player can force a win, or whether it will always
    lose against a perfect opponent.
    
    
    This algorithm explores the game by using several times the Negamax
    algorithm, always starting at the initial state of the game, but
    taking increasing depth (in the list ai_depths) until the score of
    the initial condition indicates that the first player will certainly
    win or loose, in which case it stops.
    The use of transposition table leads to speed gain as the results
    of shallower searches are used to help exploring the deeper ones.
        
    Parameters
    -----------
    
    ai_depths:
      List of AI depths to try (e.g. [5,6,7,8,9,10])
      
      
    win_score:
      Score above which a score means a win.
    
    scoring:
      Scoring function (see doc of class Negamax)
    
    tt:
      An optional transposition table to speed up computations.
    
    verbose:
      If set to ``True``, will print a summary of the best move
      after each depth tried.
        
    Returns
    --------
    
    (result, depth, move, tt):
      As below
    
    result: 
      Either 1 (certain victory of the first player) or -1
      (certain defeat) or 0 (either draw, or the search was not
      deep enough)
      
    depth:
      The minimal number of moves before victory (or defeat)
    
    move:
      Best move to play for the first player.
    
    tt:
      Will be None if ``use_tt`` was set to false, else will be a
      transposition table containing all the relevant situations to play
      a perfect game and can be used with ``AI_player(tt)``
      
    """
    
    if not hasattr(game, 'players'): # the user provided a Game class
        game = game(players = [AI_Player(None), AI_Player(None)])
    
    for depth in ai_depths:
        ai = Negamax(depth, scoring, tt= tt)
        ai(game)
        alpha = ai.alpha
        if verbose:
             print( "d:%d, a:%d, m:%s"%(depth, alpha, str(game.ai_move)))
        if abs(alpha) >= win_score:
            break
    
    # 1:win, 0:draw, -1:defeat
    result = (+1 if alpha>= win_score else (
             -1 if alpha <= -win_score else 0))
    
    return result, depth, game.ai_move


def df_solve(game, win_score, maxdepth=50, tt=None, depth=0):
    """ 
    Solves a game using a depth-first search: the game is explored until
    endgames are reached.
    
    The endgames are evaluated to see if there are victories or defeats.
    Then, a situation in which every move leads to a defeat is labelled
    as a (certain) defeat, and a situation in which one move leads to a
    (certain) defeat of the opponent is labelled as a (certain) victory.
    Situations are evaluated until the initial condition receives a label
    (victory or defeat). Draws are also possible.
    
    This algorithm can be faster but less informative than ``id_solve``,
    as it does not provide 'optimal' strategies (like shortest path to
    the victory). It returns simply 1, 0, or -1 to indicate certain
    victory, draw, or defeat of the first player.
        
    Parameters
    -----------
    
    game:
      An Game instance, initialized and ready to be played.
      
    win_score:
      Score above which a score means a win.
    
    maxdepth:
      Maximal recursion depth allowed.
    
    tt:
      An optional transposition table to speed up computations.
      
    
    depth:
      Index of the current depth (don't touch that).
      
    Returns
    --------
    
    result
      Either 1 (certain victory of the first player) or -1
      (certain defeat) or 0 (either draw, or the search was not
      deep enough)
    
    """
    
    
    # Is there a transposition table and is this game in it ?
    lookup = None if (tt is None) else tt.lookup(game)
    if lookup != None:
        return lookup['value']
        
    if (depth == maxdepth):
        raise "Max recursion depth reached :("
    
    if game.is_over():
        score = game.scoring()
        value = 1 if (score>=win_score) else (-1 if -score>=win_score else 0)
        tt.store(game=game, value=value, move=None)
        return  value
    
    possible_moves = game.possible_moves()
    
    state = game
    unmake_move = hasattr(state, 'unmake_move')
    
    best_value, best_move = -1, None
    
    for move in possible_moves:
        
        if not unmake_move:
            game = state.copy() # re-initialize move
        
        game.make_move(move)
        game.switch_player()
        
        move_value = - df_solve(game,  win_score,  maxdepth, tt, depth+1)
        
        if unmake_move:
            game.switch_player()
            game.unmake_move(move)
        
        if move_value == 1:
            tt.store(game=state, value=1, move=move)
            return move_value
        
        if move_value == 0 and best_value==-1:
            # Is forcing a draw possible ?
            best_value = 0
            best_move = move
    
    tt.store(game=state, value=best_value, move=best_move)
    
    return best_value
