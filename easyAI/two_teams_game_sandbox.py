from easyAI.TwoTeamsGame import TwoTeamsGame, AbstractOrderedPlayerSelector

from easyAI import Human_Player

class MyGame(TwoTeamsGame):
    """
    a dummy class for making experiments. With this script it ends up at 4 moves, and nothing happens :-)
    """

    def make_move(self, move):
        print(str(self.player.name) + ' makes ' + move)

    def is_over(self):
        return False

    def show(self):
        print('Possible moves: ' + str(self.possible_moves()))

    def setup_game(self):
        pass

    def possible_moves(self):
        return ['1']

class MyPlayerSelector(AbstractOrderedPlayerSelector):
    def filter_team(self, team):
        return team



g = MyGame([Human_Player()], [Human_Player()], MyPlayerSelector)
g.play(nmoves=4)
