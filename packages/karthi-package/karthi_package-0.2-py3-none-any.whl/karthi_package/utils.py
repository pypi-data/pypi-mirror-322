import numpy as np

def reshape_array(arr, new_shape):
    """Reshapes a NumPy array into the given shape."""
    return np.reshape(arr, new_shape)

def create_random_array(shape):
    """Creates a NumPy array of random values with the given shape."""
    return np.random.rand(*shape)

def array_to_string(arr):
    """Converts a NumPy array into a string representation."""
    return np.array2string(arr)
