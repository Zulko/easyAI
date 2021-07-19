Reference Manual
================

Games
-----

.. autoclass:: easyAI.TwoPlayerGame
   :members:
   :show-inheritance:


Players
-------

.. autoclass:: easyAI.Human_Player
   :show-inheritance:
   
.. autoclass:: easyAI.AI_Player
   :show-inheritance:

AI algorithms
-------------

.. autoclass:: easyAI.AI.Negamax
   :members:
   :show-inheritance:

.. autoclass:: easyAI.AI.NonRecursiveNegamax
   :members:
   :show-inheritance:

.. autoclass:: easyAI.AI.DUAL
   :members:
   :show-inheritance:

.. autoclass:: easyAI.AI.SSS
   :members:
   :show-inheritance:

   
Transposition tables
--------------------

.. autoclass:: easyAI.AI.TranspositionTable
   :members:
   :show-inheritance:
   
Solving Games
-------------

.. autofunction:: easyAI.AI.solving.solve_with_iterative_deepening

.. autofunction:: easyAI.AI.solving.solve_with_depth_first_search
