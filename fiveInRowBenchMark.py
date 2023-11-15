from board import Board
import numpy as np
from time import time
from OLD import GoBoard
import random
import cProfile
import pstats

count = 100_000


def check():
    b = Board(size=7)
    temp = False
    b._inner[:] = np.random.randint(low=0, high=3, size=(7, 7))
    for i in range(count):
        temp = b.hasFiveInRow(1)


def forLoopCheck():
    b = Board(size=7)
    temp = False
    b._inner[:] = np.random.randint(low=0, high=3, size=(7, 7))
    for i in range(count):
        temp = b.forloopChcker(1)


def oldCheck():
    b = GoBoard(7)
    temp = False

    for m in b.get_empty_points():
        b.board[m] = random.randint(0, 2)

    for i in range(count):
        temp = b.detect_five_in_a_row()


with cProfile.Profile() as p:
    check()
    res = pstats.Stats(p)
    res.sort_stats(pstats.SortKey.TIME)
    res.print_stats()

print("\n====================\n")

# with cProfile.Profile() as p:
#     forLoopCheck()
#     res = pstats.Stats(p)
#     res.sort_stats(pstats.SortKey.TIME)
#     res.print_stats()

print("\n====================\n")

with cProfile.Profile() as p:
    oldCheck()
    res = pstats.Stats(p)
    res.sort_stats(pstats.SortKey.TIME)
    res.print_stats()

# with cProfile.Profile() as p:
#     oldCheck()


# t0 = time()
# flat2Check()
# print(f'flat2 took: {time() - t0}')

# t0 = time()
# flatCheck()
# print(f'flat took: {time() - t0}')
