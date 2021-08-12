from easyAI import AI_Player, Negamax
from easyAI.games import ConnectFour, Nim
import numpy as np


def test_negamax_saves_the_next_turn_even_in_a_desperate_situation():
    """In this game of Connect4, the AI ("circles") will lose whatever it plays:

        . . . . . . .
        O . . . . . .
        X . . . . . .
        O . O . . . .
        O X X X . . .
        O O X X . . .

    However the AI is expected to go for the furthest-possible-away defeat and
    therefore play on the second column to block a 1-move win of crosses.
    """
    ai_algo = Negamax(6)
    ai_player = AI_Player(ai_algo)
    game = ConnectFour(players=[ai_player, ai_player])
    game.board = np.array(
        [
            [1, 1, 2, 2, 0, 0, 0],
            [1, 2, 2, 2, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert ai_algo(game) == 1


def test_nim_strategy_is_good():
    ai_algo = Negamax(6)
    game = Nim(piles=(4, 4))
    assert ai_algo(game) == "1,1"
