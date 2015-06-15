#contributed by mrfesol (Tomasz Wesolowski)

import random
from math import sqrt, log

class MCTS:
    """
    This implements Monte Carlo Tree Search algorithm. 
    More information at: http://mcts.ai/index.html
    The following example shows
    how to setup the AI and play a Connect Four game:
    
        >>> from easyAI import Human_Player, AI_Player, MTDf
        >>> AI = MonteCarloTreeSearch()
        >>> game = ConnectFour([AI_Player(AI),Human_Player()])
        >>> game.play()
    
    Parameters
    -----------
    
    iterations:
      Indicates how many iteration algorithm should perform.
      Larger value = More accurate result
    
    max_depth:
      How many moves in advance should the AI think ?
      (2 moves = 1 complete turn)
      
    expand_factor:
      Defines how much is algorithm willing to expand unvisited nodes.
      Usually between 0.3 and 1.0
    
    scoring:
      A function f(game)-> score. If no scoring is provided
         and the game object has a ``scoring`` method it ill be used.
      Scoring function MUST return values from interval [0, win_score]
    
    win_score:
      The largest score of game.
      It's required to run algorithm.
    
    """
        
    def __init__(self, iterations = 5000, winscore=100, depth = 20, expand_factor=0.3, scoring=None):
        self.scoring = scoring        
        self.iterations = iterations
        self.winscore = winscore
        self.max_depth = depth
        self.expand_factor = expand_factor

    def __call__(self,game):
        """
        Returns the AI's best move given the current state of the game.
        """
        rootnode = MCTSNode(state = game)

        scoring = self.scoring if self.scoring else (
                       lambda g: g.scoring() ) # horrible hack

        for i in range(self.iterations):
            node = rootnode
            state = game.copy()
            depth = 0
            
            # Select
            while node.untried == [] and node.children != []:
                node = node.select_child(self.expand_factor)
                state.make_move(node.move)
                state.switch_player()
                depth += 1
    
            # Expand
            if node.untried != []:
                m = random.choice(node.untried) 
                state.make_move(m)
                state.switch_player()
                node = node.add_child(m,state)
                
            # Rollout
            while state.possible_moves() != [] and depth < self.max_depth:
                state.make_move(random.choice(state.possible_moves()))
                state.switch_player()
                depth += 1
    
            # Backpropagate
            score = 1 - max(0, (scoring(state)/self.winscore))
            while node != None:
                node.update(score)
                node = node.parent
                score = 1-score
    
        rootnode.children.sort(key = lambda c: c.visits)
        return rootnode.children[-1].move
                
class MCTSNode:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0.0
        self.visits = 0.0
        self.untried = state.possible_moves() 
        self.last_player = state.nopponent
        
    def formula(self):
        return self.wins/self.visits 
    
    def formula_exp(self):
        return 0.3*sqrt(2*log(self.parent.visits)/self.visits)
        
    def select_child(self, expand_factor):
        """ Using the UCB1 formula to select_child a child node.
        """
        return sorted(self.children, key = lambda c: c.wins/c.visits + \
                      expand_factor*sqrt(2*log(self.visits)/c.visits))[-1]
    
    def add_child(self, m, s):
        n = MCTSNode(move = m, parent = self, state = s)
        self.untried.remove(m)
        self.children.append(n)
        return n
    
    def update(self, result):
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[P: " + str(self.last_player) + " M:" + str(self.move) + \
             " W/V:" + str(self.wins) + "/" + str(self.visits) + " F: " + \
             str(self.formula()) + " F_exp: " + str(self.formula_exp()) + "]"
