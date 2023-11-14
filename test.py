import numpy as np
import cProfile
import pstats
import time
    
class Board:
    def __init__(self, size):
        self.data = np.zeros((size, size), dtype=np.byte)
        self.size = size
        # make sliding window of size 5 for each row and col
        self.rowWindows = np.lib.stride_tricks.sliding_window_view(self.data, window_shape=(1,5))
        self.colWindows = np.lib.stride_tricks.sliding_window_view(np.transpose(self.data), window_shape=(1,5))

        # make sliding window for both diagonal directions
        # storing them as object array since the diagonals windows have different sizes
        self.antiDiagonalWindow = np.array(
            [
                np.lib.stride_tricks.sliding_window_view(np.fliplr(self.data).diagonal(offset=i), window_shape=(5,))
                for i in range(-self.size + 5, self.size - 5 + 1, 1)
            ],
            dtype=object,
        )
        self.diagonalWindow = np.array(
            [
                np.lib.stride_tricks.sliding_window_view(self.data.diagonal(offset=i), window_shape=(5,))
                for i in range(-self.size + 5, self.size - 5 + 1, 1)
            ],
            dtype=object,
        )

    def hasFiveInRow(self, value):
        return (
           np.any(np.all(self.rowWindows == value, -1),)
            or np.any(np.all(self.colWindows == value,-1), )
            # have to use concat to turn sliding window views into 2d array
            # since diagonals have different sizes
            or np.any(np.all(np.concatenate(self.antiDiagonalWindow) == value, -1), )
            or  np.any(np.all(np.concatenate(self.diagonalWindow) == value, -1), )
        )

def benchMark():
    b = Board(size=7)
    b.data[:]=np.random.randint(low=0, high=3, size=(7,7))

    for i in range(100_000):
        val = b.hasFiveInRow(1)

# t0 = time.time()
# benchMark()
# print(time.time() - t0)
with cProfile.Profile() as p:
    benchMark()
    res = pstats.Stats(p)

    res.sort_stats(pstats.SortKey.TIME)
    res.print_stats()