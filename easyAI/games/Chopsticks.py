#contributed by mrfesol (Tomasz Wesolowski)

from easyAI import TwoPlayersGame
from easyAI.Player import Human_Player
from copy import deepcopy
from easyAI.AI.DictTT import DictTT
from easyAI.AI.Hashes import JSWHashTT

class Chopsticks( TwoPlayersGame ):
    """ 
        Simple game you can play with your fingers.
        See the rules on http://en.wikipedia.org/wiki/Chopsticks_(hand_game)
        Here, for simplicity, you can do only taps and splits. 
    
        A move consists of:
            (type - split or tap, touching hand, touched hand, number of sticks 'transferred')
        for instance:
            ('split', 0, 1, 2)
        means that we transfer 2 sticks from hand 0 to hand 1
        and...
            ('tap', 1, 0, 3)
        indicates that we tap opponent's hand 0 with our hand 1 holding 3 sticks
        
        Type 'show moves' before any move and do a move by "move #XX"
    """    

    def __init__(self, players, numhands = 2):
        self.players = players
        self.numplayers = len(self.players)
        self.numhands = numhands
        self.nplayer = 1 # player 1 starts.
        
        hand = [1 for hand in range(self.numhands)]
        self.hands = [hand[:] for player in range(self.numplayers)]       
    
    def possible_moves(self):
        moves = []
        #splits
        for h1 in range(self.numhands):
            for h2 in range(self.numhands):
                if h1 == h2: continue
                hand1 = self.hands[self.nplayer-1][h1]
                hand2 = self.hands[self.nplayer-1][h2]
                for i in range(1, 1+min(hand1, 5-hand2)):
                    move = ('split', h1, h2, i)
                    if hand1 != hand2 + i and self.back_to_startstate(move) == False:
                        moves.append(move)
        
        #taps
        for i in range(self.numhands):
            for j in range(self.numhands):
                hand_player = self.hands[self.nplayer-1][i]
                hand_opp = self.hands[self.nopponent-1][j]
                if hand_player != 0 and hand_opp != 0:
                    moves.append(('tap', i, j, self.hands[self.nplayer-1][i]))
        return moves
    
    def make_move(self, move):
        type, one, two, value = move
        if type == 'split':
            self.hands[self.nplayer-1][one] -= value
            self.hands[self.nplayer-1][two] += value
        else:
            self.hands[self.nopponent-1][two] += value
            
        for player in range(self.numplayers):
            for hand in range(self.numhands):
                if self.hands[player][hand] >= 5:
                    self.hands[player][hand] = 0

    def lose(self):
        return max(self.hands[self.nplayer-1]) == 0
    
    def win(self):
        return max(self.hands[self.nopponent-1]) == 0
        
    def is_over(self):
        return self.lose() or self.win()
        
    def show(self):
        for i in range(self.numplayers):
            print("Player %d: " %(i+1)),
            for j in range(self.numhands):
                if self.hands[i][j] > 0:
                    print('|'*self.hands[i][j] + '\t'),
                else:
                    print('x\t'),
            print('')
                 
    def scoring(self):
        """
            Very simple heuristic counting 'alive' hands
        """
        if self.lose():
            return -100
        if self.win():
            return 100
        alive = [0] * 2
        for player in range(self.numplayers):
            for hand in range(len(self.hands[player])):
                alive[player] += (self.hands[player][hand] > 0)
        return alive[self.nplayer-1] - alive[self.nopponent-1]
    
    def ttentry(self):
        """
            Returns game entry
        """
        entry = [self.hands[i][j] for i in range(self.numplayers) for j in range(self.numhands)]
        entry = entry + [self.nplayer]
        return tuple(entry)  
    
    def back_to_startstate(self, move):
        """
            Checking if move will cause returning to start state - never-ending loop protection
        """
        nextstate = self.copy()
        nextstate.make_move(move)
        hands_min = min([min(nextstate.hands[i]) for i in range(self.numplayers)])
        hands_max = max([max(nextstate.hands[i]) for i in range(self.numplayers)])
        return hands_min == 1 and hands_max == 1
    
if __name__ == "__main__":
    from easyAI import Negamax, AI_Player, SSS, DUAL
    from easyAI.AI.TT import TT
    ai_algo_neg = Negamax(4)
    ai_algo_sss = SSS(4)
    dict_tt = DictTT(32, JSWHashTT())
    ai_algo_dual = DUAL(4, tt=TT(dict_tt))
    Chopsticks( [AI_Player(ai_algo_neg),AI_Player(ai_algo_dual)]).play()  #first player never wins
    
    print '-'*10
    print 'Statistics of custom dictionary:'
    print 'Calls of hash: ', dict_tt.num_calls
    print 'Collisions: ', dict_tt.num_collisions