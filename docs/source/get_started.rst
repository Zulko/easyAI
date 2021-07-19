Get Started With easyAI 
========================

The best way to get started is to have a look at :ref:`a-quick-example`. What follows is a summary of all there is to know about easyAI (you can also find these informations in the documentation of the code).

Defining a game
---------------

To define a new game, make a subclass of the class ``easyAI.TwoPlayerGame``, and define these methods:
    
    - ``__init__(self, players, ...)`` : initialization of the game
    - ``possible_moves(self)`` : returns of all moves allowed
    - ``make_move(self, move)``: transforms the game according to the move
    - ``is_over(self)``: check whether the game has ended
    
The following methods are optional:
    
    - ``show(self)`` : prints/displays the game
    - ``scoring``: gives a score to the current game (for the AI)
    - ``unmake_move(self, move)``: how to unmake a move (speeds up the AI)
    - ``ttentry(self)``: returns a string/tuple describing the game.
    - ``ttrestore(self, entry)``: use string/tuple from ttentry to restore a game.
    
The ``__init__`` method *must* do the following actions:
    
- Store ``players`` (which must be a list of two Players) into
  self.players
- Tell which player plays first with ``self.current_player = 1 # or 2``
    
When defining ``possible_moves``, ``scoring``, etc. you must keep in mind that you are in the scope of the *current player*. More precisely, a subclass of TwoPlayerGame has the following attributes that indicate whose turn it is. These attributes can be used but should not be overwritten:
    
    - ``self.player`` : the current Player (e.g. a ``Human_Player()``).
    - ``self.opponent`` :  the current Player's opponent (Player). 
    - ``self.current_player``: the number (1 or 2) of the current player.
    - ``self.opponent_index``: the number (1 or 2) of the opponent.
    - ``self.nmove``: How many moves have been played so far ?

To start a game you will write something like this ::
    
    game = MyGame(players = [player_1, player_2], *other_arguments)
    history = game.play() # start the match !

When the game ends it stores the history into the variable ``history``. The history is a list *[(g1,m1),(g2,m2)...]* where *gi* is a copy of the game after i moves and *mi* is the move made by the player whose turn it was. So for instance: ::
    
    history = game.play()
    game8, move8 = history[8]
    game9, move9 = history[9]
    game8.make_move( move8 ) # Now  game8 and game9 are alike.


Human and AI players
---------------------


The players can be either a ``Human_Player()`` (which will be asked interactively which moves it wants to play) or a ``AI_Player(algo)``, so you will have for instance ::
    
    game = MyGame( [ Human_Player(), AI_Player(algo) ])
    
If you are a human player you will be asked to enter a move when it is your turn. You can also enter ``show moves`` to have a list of all moves allowed, or ``quit`` to quit.

The variable `algo` is any function ``f(game)->move``. It can be an algorithm that determines the best move by thinking N turns in advance: ::
    
    from easyAI import AI_Player, Negamax
    ai_player = AI_Player( Negamax(9) )
    
Or a transposition table (see below) filled in a previous game: ::

    ai_player = AI_Player( transpo_table )

The Negamax algorithm will always look for the shortest path to victory, or the longest path to defeat. It is possible to go faster by not optimizing this (the disadvantage being that the AI can then make *suicidal* moves if it has found that it will eventually lose against a perfect opponent). To do so, you must provide the argument ``win_score`` to Negamax which indicates above which score a score is considered a win. Keep in mind that the AI adds maluses to the score, so if your scoring function looks like this ::
    
    scoring = lambda game: 100 if game.win() else 0

you should write ``Negamax(9, win_score=90)``.


Interactive Play
----------------

If you are needing to be more interactive with the game play, such as when integrating with other frameworks, you can use the ``get_move`` and ``play_move`` methods instead. ``get_move`` get's an AI player's decision. ``play_move`` executes a move (for either player).  To illustrate ::

    game.play()

is functionally the same as ::

    while not game.is_over():
        game.show()
        if game.current_player==1:  # we are assuming player 1 is a Human_Player
            poss = game.possible_moves()
            for index, move in enumerate(poss):
                print("{} : {}".format(index, move))
            index = int(input("enter move: "))
            move = poss[index]
        else:  # we are assuming player 2 is an AI_Player
            move = game.get_move()
            print("AI plays {}".format(move))
        game.play_move(move)


Solving a game
---------------

You can try to solve a game (i.e. determine who will win if both players play perfectly and extract a winning strategy). There are two available algorithms to do so:

**solve_with_iterative_deepening** solves a game using iterative deepening: it explores the game by using several times the Negamax algorithm, always starting at the initial state of the game, but taking increasing depth (in the list ai_depths) until the score of the initial condition indicates that the first player will certainly win or loose, at which case it stops: ::
    
    from easyAI import solve_with_iterative_deepening
    r,d,m = solve_with_iterative_deepening( MyGame, ai_depths=range(2,20), win_score=100)

Note that the first argument can be either a game instance or a game class. We obtain ``r=1``, meaning that if both players play perfectly, the first player to play can always win (-1 would have meant always lose), ``d=10``, which means that the wins will be in ten moves (i.e. 5 moves per player) or less, and ``m='3'``, which indicates that the first player's first move should be ``'3'``.


**solve_with_depth_first_search** solves a game using a depth-first search (therefore it cannot be used for games that can have an infinite number of moves). The game is explored until endgames are reached and these endgames are evaluated to see if their are victories or defeats (or draws). Then, a situation in which every move leads to a defeat is labelled as a (certain) defeat, and a situation in which one move leads to a (certain) defeat of the opponent is labelled as a (certain) victory. This way we come back up to the root (initial condition) which receives a label, which is returned. ::

    from easyAI import solve_with_depth_first_search
    game = MyGame(players = [... , ...]) # the players are not important
    tt = TranspositionTable() # optional, will speed up the algo
    r = solve_with_depth_first_search(game, winscore= 90, tt = tt)

After this ``r`` is either -1 (certain defeat of the first player against a perfect opponent), 0 (it is possible to force a draw, but not to win), or 1 (certain victory if the first player plays perfectly).
 

