I am trying to write a function that checks if there is at least one of "five in a row" of a number in a 2d array, in row, column, and diagonal directions. For example, the following 2d array has a five in a row in the first column and the main diagonal. The array to check can be any square matrix with n >= 5, but I'll most likely be working with 7x7 ones. 

```python3
A = np.array(
[
    [0, 2, 3, 4, 5, 6],
    [1, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [1, 1, 0 ,1, 0, 0],
    [1, 1, 0, 0, 1, 0],
    [1, 1, 0, 0, 1, 0]
]
)

```

My attempt at this looks like the following
```python
import numpy as np
import cProfile
import pstats
class Board:
    def __init__(self, size):
        self.data = np.zeros((size, size), dtype=np.byte)
        self.size = size
        # make sliding window of size 5 for each row and col
        self.rowWindows = np.lib.stride_tricks.sliding_window_view(self.data, window_shape=(1,5))
        self.colWindows = np.lib.stride_tricks.sliding_window_view(np.transpose(self.data), window_shape=(1,5))

        # make sliding window for both diagonal directions
        self.diagonals = []
        for i in range(-self.size+5, self.size - 5 + 1, 1):
            self.diagonals.extend(
                np.lib.stride_tricks.sliding_window_view(self.data.diagonal(offset=i), window_shape=(5,))
            )
            self.diagonals.extend(
                np.lib.stride_tricks.sliding_window_view(np.transpose(self.data).diagonal(offset=i), window_shape=(5,))
            )
        
        self.diagonals = np.array(self.diagonals, dtype=object)

    def hasFiveInRow(self, value):
        # return true if any of the window is all equal to value
        return (
            np.any(np.all(self.rowWindows == value, axis=-1))
            or np.any(np.all(self.colWindows == value, axis=-1))
            or np.any(np.all(self.diagonals == value, axis=-1))
        )


def benchMark():
    b = Board(size=7)
    b.data[:]=np.random.randint(low=0, high=3, size=(7,7))

    for i in range(100_000):
        val = b.hasFiveInRow(1)


with cProfile.Profile() as p:

    benchMark()
    res = pstats.Stats(p)
    res.sort_stats(pstats.SortKey.TIME)
    res.print_stats()
```

The resulting performance is not too bad but I would like to improve it if possible since I am using it as a part of a games ai tree search and will have to call the function very large number of times. I am thinking the `np.any(np.all(windows))` is not ideal here since it has to create many boolean array to be reduced to a single value. 

The cProfile logs is showing a large number of calls to 'reduce', 'dictcomp', and _wrapreduction' etc, which are taking a long time to finish.

Is there a better way to look for this pattern? I only need to check if this pattern occurs at least once as a boolean, although getting the exact position and number of occurances would be nice.