from copy import deepcopy


class TwoTeamsGame:

    def play(self, nmoves=1000, verbose=True):

        history = []

        if verbose:
            self.show()

        for self.nmove in range(1, nmoves + 1):

            if self.is_over():
                break

            move = self.player.ask_move(self)
            history.append((deepcopy(self), move))
            self.make_move(move)

            if verbose:
                self.show()

            self.switch_player()

        history.append(deepcopy(self))

        return history

    #@property
    #def nopponent(self):
     #   return 2 if (self.nplayer == 1) else 1


    @property
    def opponent_team(self):
       return self.current_opponent_team()

    @property
    def player(self):
        return self.current_player()

    def current_player(self):
        return self.player_selector.current_player()

    def current_opponent_team(self):
        return self.player_selector.opponent_team()

    def switch_player(self):
        self.player_selector.next_player()

    def copy(self):
        return deepcopy(self)

    def get_move(self):
        """
        Method for getting a move from the current player. If the player is an
        AI_Player, then this method will invoke the AI algorithm to choose the
        move. If the player is a Human_Player, then the interaction with the
        human is via the text terminal.
        """
        return self.player.ask_move(self)

    def play_move(self, move):
        """
        Method for playing one move with the current player. After making the move,
        the current player will change to the next player.

        Parameters
        -----------

        move:
          The move to be played. ``move`` should match an entry in the ``.possibles_moves()`` list.
        """
        result = self.make_move(move)
        self.switch_player()
        return result

class OrderedPlayerSelector:

    def __init__(self, team1, team2):
        self.teams = [team1, team2]
        self.move_no = 0
        self.counters = [0, 0]


    def current_player(self):

        team_id = self.move_no % 2
        team = self.teams[self.move_no % 2]

        character_id = self.counters[team_id] % len(team)

        return self.teams[team_id][character_id]

    def next_player(self):
        team_id = self.move_no % 2
        self.counters[team_id] += 1
        self.move_no += 1

    def current_team(self):
        return self.teams[(self.move_no) % 2]

    def opponent_team(self):
        return self.teams[(self.move_no + 1) % 2]