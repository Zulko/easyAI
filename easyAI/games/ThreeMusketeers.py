import numpy as np
from easyAI import TwoPlayersGame 

MOVES = np.zeros((30,4),dtype=int)

class ThreeMusketeers( TwoPlayersGame ):
    """
    rules: http://en.wikipedia.org/wiki/Three_Musketeers_%28game%29
    """
     
    def __init__(self, players):
        self.players = players
        self.board = np.array([[2,2,2,2,1],
                               [2,2,2,2,2],
                               [2,2,1,2,2],
                               [2,2,2,2,2],
                               [1,2,2,2,2]])
        self.musketeers = [(0,4),(2,2),(4,0)]
        self.nplayer=1
    
    def possible_moves(self):
        moves = []
        if self.nplayer == 2:
            for i in range(5):
                for j in range(5):
                    if self.board[i,j] == 0:
                        moves += [[k,l,i,j]
                                 for k,l in [(i+1,j),(i,j+1),(i-1,j),(i,j-1)]
                                 if 0<=k<5 and 0<=l<5 and self.board[k,l]==2]
        else:
            for i,j in self.musketeers:
                moves += [[i,j,k,l]
                          for k,l in [(i+1,j),(i,j+1),(i-1,j),(i,j-1)]
                          if (0<=k<5) and (0<=l<5) and self.board[k,l]==2]
                
        if moves == []:
            moves = ['None']
            
        return moves
            
    
    def make_move(self, move):
        """ move = [y1, x1, y2, x2] """
        
        if move == 'None':
            return
        
        self.board[move[0],move[1]] = 0
        self.board[move[2],move[3]] = self.nplayer
        if self.nplayer == 1:
            self.musketeers.remove( (move[0],move[1]))
            self.musketeers.append( (move[2],move[3]))
            
    
    def unmake_move(self, move):
        
        if move == 'None':
            return
        
        self.board[move[0],move[1]] = self.nplayer
        self.board[move[2],move[3]] = 0
        if self.nplayer == 1:
            self.board[move[2],move[3]] = 2
            self.musketeers.remove( (move[2],move[3]))
            self.musketeers.append( (move[0],move[1]))
    
    def win(self):
        a,b,c = self.musketeers
        aligned = (a[0]==b[0] and b[0]==c[0]) or (a[1]==b[1] and b[1]==c[1])
        if self.nplayer == 1:
            return not(aligned) and (self.possible_moves() == ['None'])
        else:
            return aligned
    
    def is_over(self):
        self.haswon = self.win() 
        return self.haswon
    
    def scoring(self):
        if self.haswon != None:
            haswon = self.haswon
            self.haswon = None
            return 100 if haswon else 0
        return 100 if self.win() else 0
    
    def show(self):
        print('\n'+'\n'.join(['--1-2-3-4-5']+
            ['ABCDE'[j]+ ' '+ ' '.join(['.12'[self.board[j,i]]
              for i in range(5)]) for j in range(5)]))

    def ttentry(self):
        return "".join(map(str,(self.nplayer,)+ tuple(self.board.flatten())))


if __name__ == "__main__":
    
    # In what follows we setup the AI and launch a AI-vs-AI match.
    
    from easyAI import Human_Player, AI_Player, Negamax
    from easyAI.AI import TT
    
    tt = TT()
    ai = Negamax(5, tt=tt)
    players = [AI_Player(ai) for i in [0,1]]
    game =ThreeMusketeers(players)
    game.play()

