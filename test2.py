import numpy as np
import scipy.signal

# The 2D array that we are searching in
A = np.array(
[[0, 1, 2, 3, 4, 5, 6],
[1, 0, 0, 0, 0, 0, 0],
[2, 0, 0, 0, 0, 0, 0],
[3, 0, 0, 0, 0, 0, 0],
[4, 0, 0, 0, 0, 0, 0],
[5, 0, 0, 0, 0, 0, 0],
[6, 0, 0, 0, 0, 0, 0]])

# The filter that we apply
B = np.array(
[[1, 0, 0, 0],
[1, 1, 1, 1]])

# The result of the convolution
result = scipy.signal.convolve2d(A, B, mode='valid')

# The filtered result that only contains values greater than 5
filtered = np.where(result >= 5)

# Printing the filtered result
print(result)