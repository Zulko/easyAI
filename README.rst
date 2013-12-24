easyAI
======

EasyAI (full documentation here_) is a pure-Python artificial intelligence framework for two-players abstract games such as Tic Tac Toe, Connect 4, Reversi, etc.
It makes it easy to define the mechanisms of a game, and play against the computer or solve the game.
Under the hood, the AI is a Negamax algorithm with alpha-beta pruning and transposition tables as described on Wikipedia_.


Installation
------------

if you have ``pip`` installed, type this in a terminal ::
    
    sudo pip install easyAI
    
Otherwise, dowload the source code (for instance on Github_), unzip everything into one folder and in this folder, in a terminal, type ::
    
    sudo python setup.py install

Additionnally you will need to install Numpy to be able to run some of the examples.


A quick example
----------------

Let us define the rules of a game and start a match against the AI: ::
    
    from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
    
    class GameOfBones( TwoPlayersGame ):
        """ In turn, the players remove one, two or three bones from a
        pile of bones. The player who removes the last bone loses. """
            
        def __init__(self, players):
            self.players = players
            self.pile = 20 # start with 20 bones in the pile
            self.nplayer = 1 # player 1 starts

        def possible_moves(self): return ['1','2','3']
        def make_move(self,move): self.pile -= int(move) # remove bones.
        def win(self): return self.pile<=0 # opponent took the last bone ?
        def is_over(self): return self.win() # Game stops when someone wins.
        def show(self): print "%d bones left in the pile"%self.pile
        def scoring(self): return 100 if game.win() else 0 # For the AI
    
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
*****************

Let us now solve the game: ::

    from easyAI import id_solve
    r,d,m = id_solve(GameOfBones, ai_depths=range(2,20), win_score=100)

We obtain ``r=1``, meaning that if both players play perfectly, the first player to play can always win (-1 would have meant always lose), ``d=10``, which means that the wins will be in ten moves (i.e. 5 moves per player) or less, and ``m='3'``, which indicates that the first player's first move should be ``'3'``.

These computations can be sped up using a transposition table which will store the situations encountered and the best moves for each: ::
    
    tt = DictTT()
    GameOfBones.ttentry = lambda game : game.pile # key for the table
    r,d,m = id_solve(GameOfBones, range(2,20), win_score=100, tt=tt)

After these lines are run the variable ``tt`` contains a transposition table storing the possible situations (here, the possible sizes of the pile) and the optimal moves to perform. With ``tt`` you can play perfectly without *thinking*: ::
    
    game = GameOfBones( [  AI_Player( tt ), Human_Player() ] )
    game.play() # you will always lose this game :)
    
Contribute !
------------

EasyAI is an open source software originally written by Zulko_ and released under the MIT licence. It is very small and could really do with some improvements, so if your are a Python/AI guru maybe you can contribute through Github_ . Some ideas of improvement are: AI algos for incomplete information games, better game solving strategies, (efficient) use of databases to store moves,  AI algorithms using parallelisation.

For troubleshooting and bug reports, the best for now is to ask on Github_.

.. _here: http://zulko.github.io/easyAI
.. _Wikipedia: http://en.wikipedia.org/wiki/Negamax
.. _Zulko : https://github.com/Zulko
.. _Github :  https://github.com/Zulko/easyAI
