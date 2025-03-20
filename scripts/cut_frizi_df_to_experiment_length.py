import pandas as pd
import numpy as np

def find_first_frame_with_mouse(bodypart_df, label_to_search_for):
    """
    This function finds the first index in the bodypart_df where the mouse was present,
    i.e., predicted with high likelihood.

    Parameters:
    bodypart_df (pd.DataFrame): The dataframe containing body part tracking data with likelihood scores.
    label_to_search_for (str): The specific label for which the likelihood should be checked (e.g., 'mouse').

    Returns:
    int: The index of the first frame where the mouse was detected with a likelihood greater than 0.99.
    """
    data = bodypart_df.copy()

    # find index where the mouse was present first
    centroid_data = data[f"{label_to_search_for}_likelihood"].to_numpy()

    # prints and returns the first index, where the centroid was predicted with high likelihood
    mouse_found = np.where(centroid_data > 0.99)[0][0]
    print(f"The mouse was found in frame: {mouse_found}.")
    return mouse_found


def cut_bodypart_df_to_experiment_timerange(bodypart_df, first_cut_point, second_cut_point=None):

    """
    If only a specific part of the video is of interest, the bodypart df can be cut,
    so unnecessary parts are rejected.

    Parameters:
    bodypart_df (pd.DataFrame): The dataframe to be cut.
    first_cut_point (int): The starting index for the cut.
    second_cut_point (int, optional): The ending index for the cut. If not provided, the dataframe
                                      will be cut from first_cut_point to the end.

    Returns:
    pd.DataFrame: The cut dataframe with the index reset.
    """

    data = bodypart_df.copy()

    # Slices the dataframe based on the provided cut points
    if second_cut_point is None:
        refactored_bodypart_df = data[first_cut_point:]
    else:  
        second_cut_point += first_cut_point 
        refactored_bodypart_df = data[first_cut_point:second_cut_point]

    # This resets the row index to start from 0 again, not from the "first time mouse present" index
    refactored_bodypart_df.reset_index(drop=True, inplace=True)

    return refactored_bodypart_df

