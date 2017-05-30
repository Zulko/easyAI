AI Class Descriptions
=====================

EasyAI has four AI classes available; each with their own characteristics.

Negamax with Alpha/Beta Pruning
-------------------------------

Negamax is a variation of the MiniMax algorithm. Minimax works by always considering the worst-case score for all possible moves for a set number of turns (plies) into the future. See https://en.wikipedia.org/wiki/Minimax

Negamax is a more efficient version of Minimax for games where the scoring is zero-sum. That is, when the score of the game board is exactly the opposite for each player. For example, if player A sees the game currently having a "score" of 7, then player B sees the score as -7.

This algorithmm also supports alpha/beta pruning. Instead of considering ALL branches, the algorithm ignores branches that cannot possibly be better given what it has seen so far.

For more information, see https://en.wikipedia.org/wiki/Negamax

Non-Recursive Negamax
---------------------

This variation of Negamax has the same features as the regular Negamax described above. The difference
is that the algorithm has been redesigned to not use recursion.

Recursion is where a process calls itself. For example, if function A calls function A which in turn calls function A, then it is behaving recursively. The negamax algorithm is naturally recursive. One of the problems with resursion is that it is not possible to predict the amount of memory and processing needed to finish the algorithm.

This variation instead pre-allocates a "list of states" to avoid recursion. For some games, this can dramatically improve performance.

DUAL
----

A variation of the Monte-Carlo Tree search algorithm described by L. W. Zhang and S. X. He, *The convergence of a dual algorithm for nonlinear programming*, Korean J. Comput. & Appl. Math.7 (2000), 487–506.

SSS*
----

A minimax algorithm similar to Negamax but where the pruning is much more extreme. It prunes all but one branch at each node in the decision tree.

As such, the SSS* algorithm does not always provide the ideal/right answer. But it can dramatically increase the performance of some games without sacrificing quality too much. It depends the nature of the game.

See https://en.wikipedia.org/wiki/SSS*
