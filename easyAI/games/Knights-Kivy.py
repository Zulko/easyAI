import numpy as np
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


# directions in which a knight can move
DIRECTIONS = list(map(np.array, [
    [1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]
]))

BOARD_SIZE = (5, 5)

# functions to convert "D8" into (3,7) and back...
pos2string = lambda ab: "ABCDEFGH"[ab[0]] + str(ab[1] + 1)
string2pos = lambda s: np.array(["ABCDEFGH".index(s[0]), int(s[1]) - 1])

SQUARE_COLORS = [
    (0.8, 0.8, 0.8, 1),  # empty
    (0.5, 0.5, 1.0, 1),  # player 1
    (1.0, 1.0, 0.8, 1),  # player 2
    (0.8, 0.0, 0.0, 1)   # occupied
]
SQUARE_TEXT = [
    " ",
    "K1",
    "K2",
    "X"
]

AI = Negamax(11)

class Knights(TwoPlayersGame):
    """
    Each player has a chess knight (that moves in "L") on a chessboard.
    Each turn the player moves the knight to any tile that hasn't been
    occupied by a knight before. The first player that cannot move loses.
    """

    def __init__(self, players, board_size=(8, 8)):
        self.players = players
        self.board_size = board_size
        self.board = np.zeros(board_size, dtype=int)
        self.board[0, 0] = 1
        self.board[board_size[0] - 1, board_size[1] - 1] = 2
        players[0].pos = np.array([0, 0])
        players[1].pos = np.array([board_size[0] - 1, board_size[1] - 1])
        self.nplayer = 1  # player 1 starts.

    def possible_moves(self):
        endings = [self.player.pos + d for d in DIRECTIONS]
        return [
            pos2string(e) for e in endings
            if (e[0] >= 0) and (e[1] >= 0) and
            (e[0] < self.board_size[0]) and
            (e[1] < self.board_size[1]) and  # inside the board
            (self.board[e[0], e[1]] == 0)    # and not blocked
        ]

    def make_move(self, pos):
        pi, pj = self.player.pos
        self.board[pi, pj] = 3  # 3 means blocked
        self.player.pos = string2pos(pos)
        pi, pj = self.player.pos
        self.board[pi, pj] = self.nplayer  # place player on board

    def show(self):
        print('\n' + '\n'.join(
            ['  1 2 3 4 5 6 7 8'] + [
                'ABCDEFGH'[k] + ' ' + ' '.join(
                    [['.', '1', '2', 'X'][self.board[k, i]]
                        for i in range(self.board_size[0])]
                ) for k in range(self.board_size[1])
            ] + ['']
        ))

    def lose(self):
        return self.possible_moves() == []

    def scoring(self):
        return -100 if (self.possible_moves() == []) else 0

    def is_over(self):
        return self.lose()


class KnightsKivyApp(App):

    def build(self):
        layout = BoxLayout(padding=10, orientation="vertical")

        self.msg_button = Button(text="K1, it is your turn.")
        layout.add_widget(self.msg_button)

        self.squares = [[] for _ in range(BOARD_SIZE[1])]
        for i in range(BOARD_SIZE[1]):
            h_layout = BoxLayout(padding=1)
            for j in range(BOARD_SIZE[0]):
                new_button = Button(on_press=self.do_move)
                new_button.location = (i, j)
                self.squares[i].append(new_button)
                h_layout.add_widget(new_button)
            layout.add_widget(h_layout)

        self.reset_button = Button(
            text="[start over]", on_press=self.reset_board
        )
        layout.add_widget(self.reset_button)

        self.refresh_board()

        return layout

    def do_move(self, btn):
        move = pos2string(btn.location)
        if move in self.game.possible_moves():
            self.game.play_move(move)
            self.refresh_board()
            if not self.game.is_over():
                self.msg_button.text = "AI is thinking. Please wait."
                move = self.game.get_move()
                self.game.play_move(move)
                self.msg_button.text = "K1, it is your turn."
        else:
            self.msg_button.text = "Invalid move. Try again."
        self.refresh_board()

    def refresh_board(self):
        for i in range(BOARD_SIZE[1]):
            for j in range(BOARD_SIZE[0]):
                self.squares[i][j].text = SQUARE_TEXT[self.game.board[i, j]]
                self.squares[i][j].background_color = \
                    SQUARE_COLORS[self.game.board[i, j]]
        if self.game.is_over():
            self.msg_button.text = "Game over. {} wins.".format(
                SQUARE_TEXT[self.game.nopponent]
            )

    def reset_board(self, btn):
        self.game = Knights([Human_Player(), AI_Player(AI)], BOARD_SIZE)
        self.refresh_board()


if __name__ == "__main__":
    board_size = (5, 5)
    game = Knights([Human_Player(), AI_Player(AI)], BOARD_SIZE)

    app = KnightsKivyApp()
    app.game = game
    app.run()
