.. _speedup:

How To Make The AI Faster
==========================

EasyAI has been written with clarity/simplicity and in mind, rather than speed. In this section we will see how to  make the AI run faster with a few refinements in the way the game is defined.

- Profile your code !
- Optimize (avoid recomputing things that have already been computed).
- For the most computer-intensive parts use fast libraries or code in C/Cython.

Let's play Connect 4
----------------------

So let's start. We want to play *Connect 4* (rules_) against the computer.

.. image:: http://upload.wikimedia.org/wikipedia/commons/a/ad/Connect_Four.gif
   :align: center

I chose this game because the implementation given in easyAI (see section :ref:`connect4`) is really not optimized: we will show that it can be sped up 25 times.

We load the game and start a match, with the following code: ::
    
    from easyAI.games import ConnectFour
    from easyAI import Human_Player, AI_Player, Negamax
    
    ai = Negamax(7) # AI thinks 7 moves in advance
    game = ConnectFour( [ AI_Player(ai), Human_Player() ])
    game.play()

We launch the script, and the computer plays after nine seconds... nine seconds !!! I mean, even in the 1990s it was considered slow ! So let's see what we can do about that.

First we profile the AI with: ::
    
    import cProfile
    cProfile.run("game.play(1)") # play one move, stop the game, profile

This will print every function used to play the first move, and the time taken by each function.

Cythonize what you can
-----------------------
The results of ``cProfile`` are clear: 6.7 of the 9 seconds are spent computing the function ``find_four``, which checks whether there are 4 connected pieces in the board. This is not the kind of function that python likes (many ``for`` and ``while`` loops) so we will rewrite this function in a faster language. You can write it in C and link it to python, but for this example I prefer to write it in Cython, because it integrates well with Python and the iPython Notebook (:download:`Cython code <speedup_cython.pyx>`). After the function is rewritten, we run again ::

    import cProfile
    cProfile.run("game.play(1)") # play one move and profile

Now it takes 2.7 seconds !

Use ``unmake_move``
--------------------

So what is the next bottleneck ? Apparently the function ``deepcopy`` is called a lot and takes a total of 1.4 seconds.

This problem is very much linked with the way easyAI works: when the AI thinks a few moves in advances, it creates whole copies of the entire game, on which it can experiment. In our case the AI has created 35000 copies of the game, no wonder it was slow.

A better solution is to perform a move directly on the original game, and once the move is evaluated, undo the move and continue with the same game. This is very easy to do with easyAI, all we have to do is to add a method called ``unmake_move`` to the class ConnectFour, which explains how to cancel a given move: ::
    
    def unmake_move(game, column):
        """ Unmake a move by removing the last piece of the column """
        line = (6 if (game.board[:, column].min()>0) else
            np.argmin( game.board[:, column] != 0) )
        game.board[line-1, column] = 0

Now as expected ``cProfile`` tells us that our program runs in 1.2 seconds.
Note that for some games *undoing* a move knowing just the move is not easy (sometimes it is even impossible).

Don't look twice if you have lost
----------------------------------

Now the function ``Connect4.lose()`` is responsible for half of the duration. This is the method which calls ``find_four``, to see if the opponent has won.  ``Connect4.lose()``  is really not called efficiently: first the AI checks if the player has lost with ``Connect4.lose()``, in order to know if the game is over (method `is_over`), then it computes a score, and for this it calls the function `scoring`, which will also call ``Connect4.lose()``.

It would be better if ``is_over`` could directly tell to ``scoring`` something like *we have lost, I already checked*. So let's rewrite these two functions: ::
    
    def lose(self):
        """ You lose if your opponent has four 'connected' pieces """
        self.haslost = find_four(self.board,self.opponent_index) # store result
        return self.haslost
    
    def scoring(game):
        if game.haslost !=None:
            haslost = game.haslost # use the stored result of ``lose``.
            game.haslost = None
            return -100 if haslost else 0
        else:
            return -100 if game.lose() else 0
    
Now that ``Connect4.lose()`` is called less our program runs in 0.74 seconds.

Use transposition tables
------------------------

Transposition tables store the values of already-computed moves and positions so that if the AI meets them again it will win time. To use such tables is very easy. First you need to tell easyAI how to represent a game in a simple form (a string or a tuple) to use as a key when you store the game in the table. In our example, the game will be represented by a string of 42 caracters indicating whether the different positions on the board are occupied by player 1, by player 2, or just empty. ::

    def ttentry(self):
        return "".join([".0X"[i] for i in self.board.flatten()])

Then you simply tell the AI that you want to use transposition tables: ::
    
    from easyAI import TranspositionTable
    ai = Negamax(7, scoring, tt = TranspositionTable())

The AI now runs in **0.4 seconds !** 

Transposition tables become more advantageous when you are thinking many moves in advance: Negamax(10) takes 2.4 seconds with transposition tables,  and 9.4 second without (for Connect 4 it is known that the tables help the AI a lot. In some other games they might be useless).

Solve the game first
--------------------

Not all games are solvable. But if it is possible to fully solve a game, you could solve it first, then store the results for use in your program. Using the GameOfBones example ::
    
    tt = TranspositionTable()
    GameOfBones.ttentry = lambda game : game.pile  # key for the table
    r,d,m = solve_with_iterative_deepening(GameOfBones, range(2,20), win_score=100, tt=tt)

After these lines are run the variable ``tt`` contains a transposition table storing the possible situations (here, the possible sizes of the pile) and the optimal moves to perform. With ``tt`` you can play perfectly without *thinking*: ::
    
    game = GameOfBones( [  AI_Player( tt ), Human_Player() ] )
    game.play()  # you will always lose this game :)

One could save the solved transposition table to a file using a python library such as ``pickle``. Then, your program need not recalculate the solution every time it starts. Instead it simply reads the saved tranposition table.

Conclusion
-----------

Now there are no obvious ways to gain significant speed. Maybe speeding up Python in general by using an optimized compiler like PyPy could help win a few more percents. But if you really want a fast and smart AI you may also consider other strategies like mixing algortihms, using opening books, etc.

.. _rules :
.. _here :
