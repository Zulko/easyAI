An easyAI crash course
======================


Defining a game
---------------

Defining a new game with easyAI looks like this: ::
    
    from easyAI import TwoPlayerGame
    
    class MyNewGame( TwoPlayerGame ):
    
        def __init__(self, players) :
            self.players = players 
            self.current_player= 1 # initialization. Player #1 starts.
            
        def possible_moves(self) : 
            return # all moves allowed to the current player
            
        def make_move(self, move) : # play the move !
           self.player.pos = move
            
        def is_over() : 
            return # whether the game has ended.
            
        def show() :
            print  # or display the current game
            
Then you set the AI algorithm as follows: ::
    
    from easyAI import Negamax
    
    def scoring(game):
        """ give a (heuristic) score to the game """
        return 100 if lose(game) else 0 # very basic example
    
    ai_algo = Negamax(8,scoring) # AI will think 8 moves in advance

Now you can start a game, for instance human vs. AI: ::
    
    from easyAI import Human_Player, AI_Player
    
    human = Human_Player( "Roger" ) # The name is optional :)
    ai = AI_Player( ai_algo )
    game = MyNewGame( [ human, ai ] )
    history = game.play() # Starts the game. Returns the 'history' at the end
