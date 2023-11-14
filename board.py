from typing import List, Literal

import numpy as np

BLACK = 1
WHITE = 2
EMPTY = 0
WALL = -1


def opponent(color: Literal[1, 2]):
    return (color % 2) + 1


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
        self.rowWindows = np.lib.stride_tricks.sliding_window_view(self._inner, window_shape=(1, 5))
        self.colWindows = np.lib.stride_tricks.sliding_window_view(np.transpose(self._inner), window_shape=(1, 5))
        # get all the diagonals and create sliding windows on them
        self.diagonalWindows = np.array(
            [
                np.lib.stride_tricks.sliding_window_view(self._inner.diagonal(offset=i), window_shape=(5,))
                for i in range(-self.size + 5, self.size - 5 + 1, 1)
            ],
            dtype=object,
        )
        self.antiDiagonalWindow = np.array(
            [
                np.lib.stride_tricks.sliding_window_view(np.fliplr(self._inner).diagonal(offset=i), window_shape=(5,))
                for i in range(-self.size + 5, self.size - 5 + 1, 1)
            ],
            dtype=object,
        )

        print(self.rowWindows.shape, self.diagonalWindows.shape)

        count = np.prod(self.rowWindows.shape[:2]) + np.prod(self.colWindows.shape[:2])
        for row in self.diagonalWindows:
            count += len(row)
        for row in self.antiDiagonalWindow:
            count += len(row)

        self.windows = np.empty(count, dtype=object,)
        print(self.windows.shape, count)
        index = 0
        index = self.addToWindow(self.windows, self.rowWindows, index)
        index = self.addToWindow(self.windows, self.colWindows, index)
        index = self.addToWindow(self.windows, self.diagonalWindows, index)
        self.addToWindow(self.windows, self.antiDiagonalWindow, index)

        ################### game states ###################
        self.currentColor = BLACK
        self.blackScore = 0
        self.whiteScore = 0

    def addToWindow(self, windows, toAdd, index):
        for row in toAdd:
            for col in row:
                windows[index] = col
                index += 1
        return index

    def hasFiveInRow(self, color: Literal[1, 2]):
        """
        only checks if <color> has a five in a row, does not check if the another color has five.
        returns true is five in row is found is any direction.
        """

        return (
            np.any(np.all(self.rowWindows == color, axis=-1))
            or np.any(np.all(self.colWindows == color, axis=-1))
            or np.any(np.all(self.flatAntiDiag == color, axis=-1))
            or np.any(np.all(self.flatDiagonal == color, axis=-1))
        )

    def otherFiveInRow(self, color):
        return np.any(np.all(self.windows == color, axis=-1))

    def forloopChcker(self, color):
        return self.a(color) or self.b(color) or self.c(color)

    def a(self, color):
        for i in range(self.size):
            count = 0
            for k in range(self.size):
                if self._inner[i][k] == color:
                    count += 1
                else:
                    count = 0
            if count >= 5:
                return True
        return False

    def b(self, color):
        for i in range(self.size):
            count = 0
            for k in range(self.size):
                if self._inner[k][i] == color:
                    count += 1
                else:
                    count = 0
            if count >= 5:
                return True
        return False

    def c(self, color):
        for line in self.diagonals:
            count = 0
            for val in line:
                if val == color:
                    count += 1
                else:
                    count = 0

            if count >= 5:
                return True
        return False

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
            [0, 1, 1, 0, 1, 1, 6,],
            [7, 8, 1, 10, 11, 12, 13],
            [14, 15, 0, 0, 18, 1, 20],
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
