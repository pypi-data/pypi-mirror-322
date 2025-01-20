import numpy as np

def add_arrays(arr1, arr2):
    """Adds two NumPy arrays element-wise."""
    return np.add(arr1, arr2)

def multiply_arrays(arr1, arr2):
    """Multiplies two NumPy arrays element-wise."""
    return np.multiply(arr1, arr2)

def mean_of_array(arr):
    """Calculates the mean of a NumPy array."""
    return np.mean(arr)

def transpose_matrix(matrix):
    """Transposes a given 2D NumPy array (matrix)."""
    return np.transpose(matrix)