inf = 1000000
eps = 0.001

def mt(game, gamma, depth, origDepth, scoring, tt=None):
    """
    This implements Memory-Enhanced Test with transposition tables.
    This method is not meant to be used directly.
    This implementation is inspired by paper:
    http://arxiv.org/ftp/arxiv/papers/1404/1404.1515.pdf
    """
    
    # Is there a transposition table and is this game in it ?
    lookup = None if (tt is None) else tt.lookup(game)
    possible_moves = None
    lowerbound, upperbound = -inf, inf
    best_move = None
    
    if lookup != None and lookup['depth'] >= depth:
        # The game has been visited in the past
        lowerbound, upperbound = lookup['lowerbound'], lookup['upperbound']
        if lowerbound > gamma:
            if depth == origDepth:
                game.ai_move = lookup['move']
            return lowerbound
        if upperbound < gamma:
            if depth == origDepth:
                game.ai_move = lookup['move']
            return upperbound
            
    bestValue = -inf
    
    if (depth == 0) or game.is_over():
        score = game.scoring()
        
        if score != 0:
            score = (score - 0.99*depth*abs(score)/score)
        
        lowerbound = upperbound = bestValue = score
    else:
        ngame = game
        unmake_move = hasattr(game, 'unmake_move')
        possible_moves = game.possible_moves()
        best_move = possible_moves[0]
    
        if not hasattr(game, 'ai_move'):
            game.ai_move = best_move
        
        for move in possible_moves:
            if bestValue >= gamma: break
            
            if not unmake_move:
                ngame = game.copy()
                
            ngame.make_move(move)
            ngame.switch_player()

            move_value = -mt(ngame, -gamma, depth-1, origDepth, scoring, tt)
            if bestValue < move_value:
                bestValue = move_value
                best_move = move
            
            if unmake_move:
                ngame.switch_player()
                ngame.unmake_move(move)
                
        if bestValue < gamma:
            upperbound = bestValue
        else:
            if depth == origDepth:
                game.ai_move = best_move
            lowerbound = bestValue
            
    if tt != None:
        
        if depth > 0 and not game.is_over():
            assert best_move in possible_moves
            tt.store(game = game, 
                     lowerbound = lowerbound, upperbound = upperbound,
                     depth = depth,
                     move = best_move)
            
    return bestValue


def mtd(game, first, next, depth, scoring, tt = None):
    """
    This implements Memory-Enhanced Test Driver.
    This method is not meant to be used directly.
    It's used by several algorithms from MT family, i.e see ``easyAI.SSS``
    For more details read following paper:
    http://arxiv.org/ftp/arxiv/papers/1404/1404.1515.pdf
    """
    bound, bestValue = first, first
    lowerbound, upperbound = -inf, inf
    while True:
        bound = next(lowerbound, upperbound, bestValue)
        bestValue = mt(game, bound - eps, depth, depth, scoring, tt)
        if bestValue < bound:
            upperbound = bestValue
        else:
            lowerbound = bestValue
        if lowerbound == upperbound:
            break
    return bestValue