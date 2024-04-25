import numpy as np


def fill_missing_values(array):
    nan_indices = np.isnan(array)
    array[nan_indices] = np.interp(np.flatnonzero(nan_indices), np.flatnonzero(~nan_indices), array[~nan_indices])
    return array

# Example usage:
array = np.array([1, 1.2, 0.3, np.nan, np.nan, np.nan, 0.8])
filled_array = fill_missing_values(array)
print(filled_array)
