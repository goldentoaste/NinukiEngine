

from player import Player
from board import Board, BLACK, EMPTY, WHITE
import numpy as np
import numpy.random as npRandom

class AlphaBetaPlayer(Player):
    
    def __init__(self, board: Board):
        self.board = board
        
    def genMove(self, color):
        # TODO do the alpha beta thing here
        
        assert color == self.board.currentColor

        moves = npRandom.Generator.shuffle(self.board.emptyPoints()) 
        draws = []
        for m in moves:
            win = self.board.play(*m, color)
            if win:
                return m
            
            score = self.alphaBeta(-2, 2, self.board.currentColor == BLACK)

            if score == 1:
                return m
            elif score == 0:
                draws.append(m)
        
        return 
    
    def alphaBeta(self,  alpha, beta, isMaxPlayer):
        '''
        assuming MaxPlayer is black
        '''
        moves = npRandom.Generator.shuffle(self.board.emptyPoints())  # any empty is playable

        color = self.board.currentColor
        if len(moves) == 0:
            return 0 # score for draw

        if isMaxPlayer:
            score = -2 # lower than any possible score
            for move in moves:
                win  = self.board.play(*move,color)

                if win: # TODO - any kinda of terminal condition here, such as depth limit
                    score = max(1, score)
                else: # TODO - this stage is not terminal for other reasons
                    score = max(score, self.alphaBeta(alpha, beta, False)) # game not end yet, recurse
                
                self.board.undo()

                if score > beta:
                    break 
                
                alpha = max(alpha, score)

            return score
        else:
            score = 2

            for move in moves:
                win = self.board.play(*move, color)    

                if win:        
                    score = min(-1, score)
                else:
                    score = min(score, self.alphaBeta((alpha, beta, True)))
                
                self.board.undo()

                if score < alpha:
                    break
                
                beta = min(beta, score)
            
            return score
        