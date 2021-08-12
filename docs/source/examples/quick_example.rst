.. _a-quick-example:

A quick example
================

Let us define the rules of a game and start a match against the AI: ::
    
    from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
    
    class GameOfBones( TwoPlayerGame ):
        """ In turn, the players remove one, two or three bones from a
        pile of bones. The player who removes the last bone loses. """
            
        def __init__(self, players=None):
            self.players = players
            self.pile = 20 # start with 20 bones in the pile
            self.current_player = 1 # player 1 starts

        def possible_moves(self): return ['1','2','3']
        def make_move(self,move): self.pile -= int(move) # remove bones.
        def win(self): return self.pile<=0 # opponent took the last bone ?
        def is_over(self): return self.win() # Game stops when someone wins.
        def show(self): print "%d bones left in the pile"%self.pile
        def scoring(self): return 100 if self.win() else 0 # For the AI
    
    # Start a match (and store the history of moves when it ends)
    ai = Negamax(13) # The AI will think 13 moves in advance 
    game = GameOfBones( [ Human_Player(), AI_Player(ai) ] )
    history = game.play()
    
Result: ::
    
    20 bones left in the pile
    
    Player 1 what do you play ? 3

    Move #1: player 1 plays 3 :
    17 bones left in the pile

    Move #2: player 2 plays 1 :
    16 bones left in the pile
    
    Player 1 what do you play ?

Solving the game
-----------------

Let us now solve the game: ::

    from easyAI import solve_with_iterative_deepening
    r,d,m = solve_with_iterative_deepening(GameOfBones(), ai_depths=range(2,20), win_score=100)

We obtain ``r=1``, meaning that if both players play perfectly, the first player to play can always win (-1 would have meant always lose), ``d=10``, which means that the wins will be in ten moves (i.e. 5 moves per player) or less, and ``m='3'``, which indicates that the first player's first move should be ``'3'``.

These computations can be sped up using a transposition table which will store the situations encountered and the best moves for each: ::
    
    tt = TranspositionTable()
    GameOfBones.ttentry = lambda game : game.pile # key for the table
    r,d,m = solve_with_iterative_deepening(GameOfBones(), range(2,20), win_score=100, tt=tt)

After these lines are run the variable ``tt`` contains a transposition table storing the possible situations (here, the possible sizes of the pile) and the optimal moves to perform. With ``tt`` you can play perfectly without *thinking*: ::
    
    game = GameOfBones( [  AI_Player( tt ), Human_Player() ] )
    game.play() # you will always lose this game :)
