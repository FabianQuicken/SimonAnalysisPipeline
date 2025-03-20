from likelihood_filter import likelihood_filtering
import pandas as pd
import numpy as np


def calc_coordinate_center(x_coords_list, y_coords_list):
    """
    This function returns the center of a given list of coordinates.
    Therefore, the coordinates should be opposites, e.g. the north, south, west and east position of a circle.
    The arguments need to be lists of integers or floats.
    """
    sum_x_coords = sum(x_coords_list)
    sum_y_coords = sum(y_coords_list)

    center_x_coord = sum_x_coords / len(x_coords_list)
    center_y_coord = sum_y_coords / len(y_coords_list)

    return center_x_coord, center_y_coord

def add_dish_center_to_bodypart_df(bodypart_df, dish_center_x, dish_center_y, column_name=str):
    """
    This function will add x and y coordinates to the bodypart_df. Altough being single arguments, 
    to keep the integrity of the df, the columns will have the length of the dataframe. 
    """
    dish_center_x_array = np.zeros(len(bodypart_df))
    dish_center_y_array = np.zeros(len(bodypart_df))
    for i in range(len(dish_center_x_array)):
        dish_center_x_array[i] = dish_center_x
        dish_center_y_array[i] = dish_center_y
    bodypart_df[f"{column_name}_x"] = dish_center_x_array
    bodypart_df[f"{column_name}_y"] = dish_center_y_array
    

def get_high_likelihood_dish_coordinates(df, 
                                         object_edge_names = ["leftpetrileft",
                                                                "leftpetriright",
                                                                "leftpetritop",
                                                                "leftpetribottom"
                                                                ], 
                                        thresh = 0.99):

    x_coords = []
    y_coords = []
    data = df.copy()

    # filters for good petri dish edge predictions and appends the edges x and y coordinate to separate lists
    for edge_name in object_edge_names:
        data_x_filtered = likelihood_filtering(df = data, likelihood_row_name=f"{edge_name}_x", filter_val=thresh)
        x_values = data_x_filtered[f"{edge_name}_x"].to_numpy()
        
        
        data_y_filtered = likelihood_filtering(df = data, likelihood_row_name=f"{edge_name}_y", filter_val=thresh)
        y_values = data_y_filtered[f"{edge_name}_y"].to_numpy()
        
        
        # Check if there are any values left after filtering
        if len(x_values) > 0:
            x_coords.append(x_values[0])
        else:
            x_coords.append(None)  # or some other placeholder

        if len(y_values) > 0:
            y_coords.append(y_values[0])
        else:
            y_coords.append(None)  # or some other placeholder

    return x_coords, y_coords






