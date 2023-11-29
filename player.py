

from board import Board


class Player:
    def __init__(self, board: Board):
        pass
    
    def genMove(self, color):
        # given color, return a move this player should play
        return (0,0)
    
    def replaceBoard(self, board: Board):
        self.board = board