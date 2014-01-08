easyAI
======

EasyAI is a pure-Python artificial intelligence framework for two-players abstract games such as Tic Tac Toe, Connect 4, Reversi, etc.
It makes it easy to define the mechanisms of a game, and play against the computer or solve the game (see :ref:`a-quick-example`).
Under the hood, the AI is a Negamax algorithm with alpha-beta pruning and transposition tables as described on Wikipedia_.

EasyAI has been written with clarity/simplicity in mind, rather than speed, so it can be slow, but there are fixes (see :ref:`speedup`).

User's Guide
--------------

.. toctree::
   :maxdepth: 1
   
   installation
   get_started
   examples/examples
   ref

EasyAI is an open source software originally written by Zulko_ and released under the MIT licence. It is very small and could really do with some improvements, so if you are a Python/AI guru maybe you can contribute through Github_ . Some ideas of improvement are: AI algos for incomplete information games, better game solving strategies, (efficient) use of databases to store moves,  AI algorithms using parallelisation.

For troubleshooting and bug reports, the best for now is to ask on Github_.

Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. raw:: html

        <a href="https://github.com/Zulko/easyAI">
        <img style="position: absolute; top: 0; right: 0; border: 0;"
        src="https://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png"
        alt="Fork me on GitHub"></a>

.. _Wikipedia: http://en.wikipedia.org/wiki/Negamax
.. _`game design`:
.. _`AI design/optimization`:
.. _Zulko : https://github.com/Zulko
.. _Github :  https://github.com/Zulko/easyAI
