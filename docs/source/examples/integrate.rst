.. _ExamplesOfGameIntegration:

Integrating easyAI with other frameworks
========================================

The primary means of executing easyAI is with the ``play`` method
of TwoPlayerGame. That method handles getting human input and executing
AI functions from start to finish.

But, when using easyAI with other frameworks, one must often break down the
steps execution. For that, use the ``get_move`` method to get an AI players
decision, and the ``play_move`` to properly execute a turn.

Here are some games implementations using other frameworks provided in the
``examples`` folder of easyAI.

Tic-Tac-Toe Using Flask
-----------------------

.. literalinclude:: ../../../easyAI/games/TicTacToe-Flask.py

Game of Knights using Kivy
--------------------------

.. literalinclude:: ../../../easyAI/games/Knights-Kivy.py

