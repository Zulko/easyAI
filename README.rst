easyAI
======

EasyAI (full documentation here_) is a pure-Python artificial intelligence framework for two-players abstract games such as Tic Tac Toe, Connect 4, Reversi, etc.
It makes it easy to define the mechanisms of a game, and play against the computer or solve the game.
Under the hood, the AI is a Negamax algorithm with alpha-beta pruning and transposition tables as described on Wikipedia_.


Installation
------------

If you have ``pip`` installed, type this in a terminal ::
    
    sudo pip install easyAI
    
Otherwise, download the source code (for instance on Github_), unzip everything into one folder and in this folder, in a terminal, type ::
    
    sudo python setup.py install

Additionally you will need to install Numpy to be able to run some of the examples.


A quick example
----------------

Let us define the rules of a game and start a match against the AI:

.. code:: python
    
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
        def show(self): print ("%d bones left in the pile" % self.pile)
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

Let us now solve the game:

.. code:: python

    from easyAI import solve_with_iterative_deepening
    r,d,m = solve_with_iterative_deepening(
        game=GameOfBones(),
        ai_depths=range(2,20),
        win_score=100
    )

We obtain ``r=1``, meaning that if both players play perfectly, the first player to play can always win (-1 would have meant always lose), ``d=10``, which means that the wins will be in ten moves (i.e. 5 moves per player) or less, and ``m='3'``, which indicates that the first player's first move should be ``'3'``.

These computations can be speed up using a transposition table which will store the situations encountered and the best moves for each:

.. code:: python

    tt = TranspositionTable()
    GameOfBones.ttentry = lambda game : game.pile # key for the table
    r,d,m = solve_with_iterative_deepening(
        game=GameOfBones(),
        ai_depths=range(2,20),
        win_score=100,
        tt=tt
    )

After these lines are run the variable ``tt`` contains a transposition table storing the possible situations (here, the possible sizes of the pile) and the optimal moves to perform. With ``tt`` you can play perfectly without *thinking*:

.. code:: python

    game = GameOfBones( [  AI_Player( tt ), Human_Player() ] )
    game.play() # you will always lose this game :)


Contribute !
------------

EasyAI is an open source software originally written by Zulko_ and released under the MIT licence. Contributions welcome! Some ideas: AI algos for incomplete information games, better game solving strategies, (efficient) use of databases to store moves,  AI algorithms using parallelisation.

For troubleshooting and bug reports, the best for now is to ask on Github_.

How releases work
*****************

Every time a MR gets merged into master, an automatic release happens:

- If the last commit's message starts with `[FEATURE]`, a feature release happens (`1.3.3 -> 1.4.0`)
- If the last commit's message starts with `[MAJOR]`, a major release happens (`1.3.3 -> 2.0.0`)
- If the last commit's message starts with `[SKIP]`, no release happens.
- Otherwise, a patch release happens (`1.3.3 -> 1.3.4`)



Maintainers
-----------

- Zulko_ (owner)
- JohnAD_


.. _here: http://zulko.github.io/easyAI
.. _Wikipedia: http://en.wikipedia.org/wiki/Negamax
.. _Zulko : https://github.com/Zulko
.. _JohnAD : https://github.com/JohnAD
.. _Github :  https://github.com/Zulko/easyAI
