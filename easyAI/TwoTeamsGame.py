from copy import deepcopy


class TwoTeamsGame:

    def __init__(self, team1, team2, player_selector):
        """
        :param team1: array of easyAI-supported objects. See Player module
        :param team2: array of easyAI-supported objects.
        :param player_selector constructor for objects of type AbstractOrderedPlayerSelector (see below)
        """
        self.player_selector = player_selector(team1, team2)
        self.setup_game()

    def setup_game(self):
        """
        put here your own initialization and so on
        :return:
        """
        raise NotImplementedError('Abstract method')

    def make_move(self, move):
        raise NotImplementedError('Abstract method')

    def show(self):
        raise NotImplementedError('Abstract method')

    def is_over(self):
        raise NotImplementedError('Abstract method')


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


    @property
    def opponent_team(self):
       return self.current_opponent_team()

    @property
    def player(self):
        return self.current_player()

    @property
    def nplayer(self):
        return self.current_player().name

    def current_player(self):
        return self.player_selector.current_player()

    def current_opponent_team(self):
        return self.player_selector.opponent_team()

    def current_team(self):
        return self.player_selector.current_team()

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

class AbstractOrderedPlayerSelector:
    """
    Base class for player selectors. Selects next player in order, the behaviour is:

    team1 - player1
    team2 - player 1

    team 1 - player 2
    team 2 - player 2

    etc

    according to rules defined in filter_team
    """

    def __init__(self, team1, team2):
        self.teams = [team1, team2]
        self.move_no = 0
        self.counters = [0, 0]

    def filter_team(self, team):
        """
        Filters an array of players. Used for return active players. For example in a RPG game may be the still alive ones
        :param team:
        :return:
        """
        raise NotImplementedError('Abstract method')

    def current_player(self):

        team_id = self._current_team_id()
        team = self.current_team()

        character_id = self.counters[team_id] % len(team)

        return team[character_id]

    def _current_team_id(self):
        return self.move_no % 2

    def _next_team_id(self):
        return (self.move_no + 1) % 2

    def next_player(self):
        """
        Moves pointer to next player
        :return:
        """
        team_id = self._current_team_id()
        self.counters[team_id] += 1
        self.move_no += 1

    def current_team(self):
        return self.filter_team(self.teams[self._current_team_id()])

    def opponent_team(self):
        return self.filter_team(self.teams[self._next_team_id()])