from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from flask import Flask, render_template_string, request, redirect, url_for, make_response


class TicTacToe(TwoPlayersGame):
    """ The board positions are numbered as follows:
            7 8 9
            4 5 6
            1 2 3
    """

    def __init__(self, players):
        self.players = players
        self.board = [0 for i in range(9)]
        self.nplayer = 1  # player 1 starts.

    def possible_moves(self):
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move) - 1] = self.nplayer

    def unmake_move(self, move):  # optional method (speeds up the AI)
        self.board[int(move) - 1] = 0

    def lose(self, who=None):
        """ Has the opponent "three in line ?" """
        if who is None:
            who = self.nopponent
        return any( [all([(self.board[c-1] == who)
                      for c in line])
                      for line in [[1,2,3],[4,5,6],[7,8,9], # horiz.
                                   [1,4,7],[2,5,8],[3,6,9], # vertical
                                   [1,5,9],[3,5,7]]]) # diagonal

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def show(self):
        print ('\n' + '\n'.join([
            ' '.join([['.', 'O', 'X'][self.board[3 * j + i]] for i in range(3)])
            for j in range(3)
        ]))

    def spot_string(self, i, j):
        return ["_", "O", "X"][self.board[3 * j + i]]

    def scoring(self):
        return -100 if self.lose() else 0

    def winner(self):
        if self.lose(who=1):
            return "AI Wins"
        return "Tie"


page_text = '''
<!doctype html>
<html>
  <head><title>Tic Tac Toe</title></head>
  <body>
    <h1>Tic Tac Toe</h1>
    <h2>{{msg}}</h2>
    <form action="" method="POST">
      <table>
        {% for j in range(2, -1, -1) %}
        <tr>
          {% for i in range(0, 3) %}
          <td>
            <button type="submit" name="choice" value="{{j*3+i+1}}" {{"disabled" if ttt.spot_string(i, j)!="_"}}>
              {{ttt.spot_string(i, j)}}
            </button>
          </td>
          {% endfor %}
        </tr>
        {% endfor %}
      </table>
      <button type="submit" name="reset">Start Over</button>
    </form>
  </body>
</html>
'''

app = Flask(__name__)
ai_algo = Negamax(6)

@app.route("/", methods=['GET', 'POST'])
def play_game():
    ttt = TicTacToe([Human_Player(), AI_Player(ai_algo)])
    game_cookie = request.cookies.get('game_board')
    if game_cookie:
        ttt.board = [int(x) for x in game_cookie.split(",")]
    if "choice" in request.form:
        ttt.play_move(request.form["choice"])
        if not ttt.is_over():
            ai_move = ttt.get_move()
            ttt.play_move(ai_move)
    if "reset" in request.form:
        ttt.board = [0 for i in range(9)]
    if ttt.is_over():
        msg = ttt.winner()
    else:
        msg = "play move"
    resp = make_response(render_template_string(page_text, ttt=ttt, msg=msg))
    c = ",".join(map(str, ttt.board))
    resp.set_cookie("game_board", c)
    return resp

if __name__ == "__main__":
    app.run()
