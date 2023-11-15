from typing import List, Literal
from collections import namedtuple
import numpy as np

undoDiff = namedtuple(
    "undoDiff",
    [
        "center",  # point
        "captures",  # points of the other color that got captured,
        "color",  # color of the center
    ],
)

boardState = namedtuple(
    "boardState",
    [
        "board",  # ndarray of the board content,
        "color",  # color to play
        "blackScore",
        "whiteScore",
    ],
)

BLACK = 1
WHITE = 2
EMPTY = 0
WALL = -1

dirs = ((0, 1), (1, 0), (1, 1), (-1, 1))
dirSigned = (*dirs, *(-d for d in dirs))


def opponent(color: Literal[1, 2]):
    return (color % 2) + 1

def t2p(move):
    # convert text to move tuple (row, col)
    # a2 -> a is col, 2 is row
    # no error checks, assume valid input
    
    # 97 is ascii for lower a
    return (int(move[1]) - 1, ord(move[0]) - 97) 

def p2t(move):
    # convert postion to text representation
    # (2,3) -> d3
    return (move[1] + 1, chr(move[0] + 97))

def t2c(color):
    # get color of text
    # also assumes valid input
    return BLACK if color == 'b' else WHITE

class Board:
    def __init__(self, size=7, iniData=None):
        """
        warning, creating a board involves pre computing the views and some setup to speed up later opertaions,
        should be repeatly creating new boards should be avoided
        """

        ################### initial data ###################
        self.size = size
        if iniData is not None:
            self.size = len(iniData)
        self.data = np.zeros((self.size + 2, self.size + 2), dtype=np.byte)
        self._inner = self.data[1:-1, 1:-1]

        # make the walls
        self.data[:, 0].fill(-1)
        self.data[:, -1].fill(-1)
        self.data[0, :].fill(-1)
        self.data[-1, :].fill(-1)

        if iniData is not None:
            self._inner[:] = np.array(iniData)

        ################## precomputing views for 5 in row ###################

        # precompute views to speed to checks
        self.rowWindows = np.lib.stride_tricks.sliding_window_view(
            self._inner, window_shape=(1, 5)
        )
        self.colWindows = np.lib.stride_tricks.sliding_window_view(
            np.transpose(self._inner), window_shape=(1, 5)
        )
        # get all the diagonals and create sliding windows on them
        self.diagonalWindows = np.array(
            [
                np.lib.stride_tricks.sliding_window_view(
                    self._inner.diagonal(offset=i), window_shape=(5,)
                )
                for i in range(-self.size + 5, self.size - 5 + 1, 1)
            ],
            dtype=object,
        )
        self.antiDiagonalWindow = np.array(
            [
                np.lib.stride_tricks.sliding_window_view(
                    np.fliplr(self._inner).diagonal(offset=i), window_shape=(5,)
                )
                for i in range(-self.size + 5, self.size - 5 + 1, 1)
            ],
            dtype=object,
        )
        self.lowDiag = -self.size + 5
        self.highDiag = self.size - 4

        ################### game states ###################
        self.currentColor = BLACK
        self.blackScore = 0
        self.whiteScore = 0

        self.history: List[undoDiff] = []
        
    

    def emptyPoints(self):
        # returns indices where the array is 0
        return np.transpose(np.where(self._inner == 0))

    def play(self, row, col, color):
        # returns true if playing the cause the win for the player of color
        # returns false other wise
        # undo history is saved by this function

        # reduce func call
        opColor = (color % 2) + 1
        data = self.data
        self._inner[row, col] = color
        self.currentColor = opColor

        # row/column check
        fiveInRow = np.any(np.all(self.rowWindows[row, col] == color, axis=-1)) or np.any(
            np.all(self.colWindows[row, col] == color, axis=-1)
        )

        # check if the position is part of a diagonal
        if self.lowDiag < row - col < self.highDiag:
            # x-y is diagonal, y-x is antidiagonal
            fiveInRow = (
                fiveInRow
                or np.any(np.all(np.all(self.diagonalWindows[row - col] == color, axis=-1)))
                or np.any(np.all(self.antiDiagonalWindow[col - row] == color, axis=-1))
            )
        if fiveInRow:
            self.history.append(undoDiff((row, col), (), color ))
            return fiveInRow
        
        # now check if this play cause any captures
        captures = []
        row, col = row + 1, col + 1
        
        for dRow, dCol in dirSigned:
            if data[row + dRow][col + dCol] == opColor and data[row + dRow * 2][col + dCol * 2] == opColor and data[row + dRow * 3][col + dCol * 3] == color:
                captures.append((row + dRow, col + dCol))
                captures.append((row + dRow*2, col + dCol * 2))
        
        captures = tuple(captures)
        # capture all the pieces
        data[captures] = EMPTY 
        
        # done playing now, add to history
        self.history.append(undoDiff(
            (row, col),
            captures,color
        ))
        
        if color == BLACK:
            self.blackScore += len(captures)
            return self.blackScore >= 10
        else:
            self.whiteScore += len(captures)
            return self.whiteScore >= 10
        

    def playNoUndo(self, row, col, color):
        # same as play, except it doesnt use history/undo, maybe this is faster
        # returns if the 'color' wins somehow by playing this move.
        
        # reduce func call
        opColor = (color % 2) + 1
        data = self.data
        self._inner[row, col] = color
        self.currentColor = opColor

        # row/column check
        fiveInRow = np.any(np.all(self.rowWindows[row, col] == color, axis=-1)) or np.any(
            np.all(self.colWindows[row, col] == color, axis=-1)
        )

        # check if the position is part of a diagonal
        if self.lowDiag < row - col < self.highDiag:
            # x-y is diagonal, y-x is antidiagonal
            fiveInRow = (
                fiveInRow
                or np.any(np.all(np.all(self.diagonalWindows[row - col] == color, axis=-1)))
                or np.any(np.all(self.antiDiagonalWindow[col - row] == color, axis=-1))
            )
        if fiveInRow:
            self.history.append(undoDiff((row, col), (), color ))
            return fiveInRow
        
        # now check if this play cause any captures
        captures = 0
        row, col = row + 1, col + 1
        
        for dRow, dCol in dirSigned:
            if data[row + dRow][col + dCol] == opColor and data[row + dRow * 2][col + dCol * 2] == opColor and data[row + dRow * 3][col + dCol * 3] == color:
                data[row + dRow, col + dCol] = EMPTY
                data[row + dRow * 2, col + dCol * 2]  = EMPTY
                captures += 2
        
        if color == BLACK:
            self.blackScore += captures
            return self.blackScore >= 10
        else:
            self.whiteScore += captures
            return self.whiteScore >= 10

    def undo(self):
        # get the lastest move
        lastMove = self.history.pop()
        opColor = (lastMove.center % 2) + 1
        self._inner[lastMove.center] = EMPTY
        self._inner[lastMove.captures] = opColor
        self.currentColor = lastMove.color

    def saveState(self):
        return boardState(
            self._inner.copy(), self.currentColor, self.blackScore, self.whiteScore
        )

    def restoreState(self, state: boardState):
        self.currentColor = state.color
        self.blackScore = state.blackScore
        self.whiteScore = state.whiteScore
        self._inner[:, :] = state.board

    def hasFiveInRow(self, color: Literal[1, 2]):
        """
        only checks if <color> has a five in a row, does not check if the another color has five.
        returns true is five in row is found is any direction.
        """

        return (
            np.any(np.all(self.rowWindows == color, axis=-1))
            or np.any(np.all(self.colWindows == color, axis=-1))
            or np.any(np.all(np.concatenate(self.diagonalWindows) == color, axis=-1))
            or np.any(np.all(np.concatenate(self.antiDiagonalWindow) == color, axis=-1))
        )

    def reset(self):
        self.blackScore = 0
        self.whiteScore = 0
        self.currentColor = BLACK
        self.data[1:-1, 1:-1].fill(0)

    def __str__(self):
        return str(self._inner)


if __name__ == "__main__":
    b = Board(
        iniData=[
            [
                0,
                1,
                1,
                0,
                1,
                1,
                6,
            ],
            [7, 8, 1, 10, 11, 12, 13],
            [14, 15, 0, 1, 18, 1, 20],
            [21, 22, 23, 0, 1, 26, 27],
            [28, 29, 30, 1, 1, 1, 34],
            [35, 36, 0, 38, 39, 40, 41],
            [42, 1, 44, 45, 46, 47, 48],
        ]
    )
    # b._inner.fill(22)
    # print(b.diagonalWindows)
    # print(b.rowWindows)
    # print(np.all(b.antiDiagonalWindow == 22, axis=-1))
    print(b.hasFiveInRow(1))
    print(b._inner)
