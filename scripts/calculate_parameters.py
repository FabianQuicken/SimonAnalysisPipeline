import numpy as np
import pandas as pd
from mathematics import euklidean_distance, punkt_in_viereck
from likelihood_filter import likelihood_filtering,likelihood_filtering_nans
from configurations import pixel_per_cm



def time_spent_sides(df,bodypart=str,edge_left=str, edge_right=str):
    data = df.copy()
    print("\nGet time spent on either cagehalf...")
    print(f"Filtering {bodypart} for time spent on either cage half.")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart+"_likelihood")
    bodypart_x = data[bodypart+"_x"]

    print("Filtering for a good petridish prediction...")
    data = likelihood_filtering(df=data, 
                                likelihood_row_name=edge_left+"_likelihood",
                                filter_val=0.95)
    data = likelihood_filtering(df=data, 
                                likelihood_row_name=edge_right+"_likelihood",
                                filter_val=0.95)    
    edge_left_x = data[edge_left+"_x"]
    edge_right_x = data[edge_right+"_x"]
    
    bodypart_x = np.array(bodypart_x)

    edge_left_x = np.array(edge_left_x)
    edge_right_x = np.array(edge_right_x)
    edge_left_x = edge_left_x[0]
    edge_right_x = edge_right_x[0]
    

    middle = (edge_left_x + edge_right_x) / 2
    print(f"The edges (left,right) are set as {round(edge_left_x)}, {round(edge_right_x)}. The midpoint is {round(middle)}.")

    is_left_values = np.where(bodypart_x < middle, 1, 0)
    is_right_values = np.where(bodypart_x > middle, 1, 0)
    is_left_values = is_left_values.astype(float)
    is_right_values = is_right_values.astype(float)
    is_left_values[np.isnan(bodypart_x)] = np.nan
    is_right_values[np.isnan(bodypart_x)] = np.nan


    """
    is_left_values = np.zeros((len(bodypart_x)))
    is_right_values = np.zeros((len(bodypart_x)))

    for i in range(len(bodypart_x)-1):
        if bodypart_x[i] < middle:
            is_left_values[i] = 1
        elif bodypart_x[i] > middle:
            is_right_values[i] = 1
        elif np.isnan(bodypart_x[i]):
            is_left_values[i] = np.nan
            is_right_values[i] = np.nan
    """

    return is_left_values,is_right_values






def distance_travelled(df,bodypart=str):
    """
    Takes a Dataframe and a bodypart as input
    calculates the distance of a keypoint
    between consequetive frames in m.
    Note: Likelihood filtering gets applied for the bodypart.
    """
    data = df.copy()
    print("\nGet distance values...")
    print(f"Filtering {bodypart} for distance calculation...")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart+"_likelihood")
    
    bodypart_x = data[bodypart+"_x"]
    bodypart_y = data[bodypart+"_y"]

    bodypart_x = np.array(bodypart_x) #transforms bodypart data into np array for easier calculation
    bodypart_y = np.array(bodypart_y)

    distance_values = np.zeros((len(bodypart_x)))
    for i in range(len(bodypart_x)-1):
        distance_values[i] = euklidean_distance(x1=bodypart_x[i],
                                                y1=bodypart_y[i],
                                                x2=bodypart_x[i+1],
                                                y2=bodypart_y[i+1])
        
        distance_values[i] = distance_values[i] / (pixel_per_cm*100) # umrechnung in meter
    return distance_values



def calculate_speed(distance_array,fps=60):
    """
    calculates the speed between frames in km/h
    """
    print("\nGet speed values...")
    #distance_values = np.array(parameter_df["distance"])
    distance_values = distance_array.copy()
    for i in range(len(distance_values)):
        distance_values[i]=((distance_values[i]*fps))*3.6 #changing m/s to km/h
    speed_between_frames = distance_values
    """
    for i in range(len(speed_between_frames)-1):
        if speed_between_frames[i] > 50:
            speed_between_frames[i] = np.nan
    """
    return speed_between_frames



def distance_bodypart_object(df, bodypart=str, object=str):
    """
    Takes a Dataframe, a bodypart and an object as strings,
    to calculate the distance between both.
    Note: Df gets likelihood filtered for bodypart first.
    Object should not move during recording, since
    the first good prediction will be set to the object location.
    """
    data = df.copy()
    print(f"\nGet distance {bodypart} to {object}...")
    print(f"Filtering {bodypart} for object distance calculation...")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart+"_likelihood")
    bodypart_x = data[bodypart+"_x"]
    bodypart_y = data[bodypart+"_y"]


    # überspringt, falls vorher schon berechnet und daher keine likelihood vorhanden:
    try:
        print("Filtering for a good object prediction...")
        data = likelihood_filtering(df=data, 
                                    likelihood_row_name=object+"_likelihood",
                                    filter_val=0.95)
    except:
        print(f"No likelihood row available. Likelihood filtering of {object} skipped.")
    object_x = data[object+"_x"].dropna()
    object_y = data[object+"_y"].dropna()
    bodypart_x = data[bodypart+"_x"]
    bodypart_y = data[bodypart+"_y"]


    bodypart_x = np.array(bodypart_x)
    bodypart_y = np.array(bodypart_y)
    object_x = np.array(object_x)
    object_y = np.array(object_y)
    object_x = object_x[0]
    object_y = object_y[0]
    print(f"{object} x-coord: {object_x}")
    print(f"{object} y-coord: {object_y}")


    distance_values = np.zeros((len(bodypart_x)))
    for i in range(len(bodypart_x)-1):
        distance_values[i] = euklidean_distance(x1=bodypart_x[i],
                                                y1=bodypart_y[i],
                                                x2=object_x,
                                                y2=object_y)
    return distance_values


def distance_bodypart_bodypart(df, bodypart_1=str, bodypart_2=str):
    """
    Takes a Dataframe and two bodyparts (can be 2 animals) as strings,
    to calculate the distance between both points
    Note: Df gets likelihood filtered for points of interest first.
    """
    data = df.copy()
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart_1+"_likelihood")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart_2+"_likelihood")
    bodypart_1_x = data[bodypart_1+"_x"]
    bodypart_1_y = data[bodypart_1+"_y"]
    bodypart_2_x = data[bodypart_2+"_x"]
    bodypart_2_y = data[bodypart_2+"_y"]

    bodypart_1_x = np.array(bodypart_1_x)
    bodypart_1_y = np.array(bodypart_1_y)
    bodypart_2_x = np.array(bodypart_2_x)
    bodypart_2_y = np.array(bodypart_2_y)

    distance_values = np.zeros((len(bodypart_1_x)))
    for i in range(len(bodypart_1_x)-1):
        distance_values[i] = euklidean_distance(x1=bodypart_1_x[i],
                                                y1=bodypart_1_y[i],
                                                x2=bodypart_2_x[i],
                                                y2=bodypart_2_y[i])
    return distance_values
    


def investigation_time(distance_values, factor = 1):
    distance_values = distance_values.copy()
    radius_threshold = factor * pixel_per_cm
    print(f"Investigation is True if nose is within {radius_threshold} pixels to the dish center.")
    is_investigating = np.zeros((len(distance_values)))
    for i in range(len(distance_values)-1):
        if distance_values[i] < radius_threshold:
            is_investigating[i] = 1
        elif np.isnan(distance_values[i]):
            is_investigating[i] = np.nan
    return is_investigating, factor

def immobile_time(speed_values, immobile_threshold = 0.1):
    speed_values = speed_values.copy()
    print("\nGet immobile time...")
    is_immobile = np.zeros((len(speed_values)))
    for i in range(len(speed_values)-1):
        if speed_values[i] < immobile_threshold:
            is_immobile[i] = 1
        elif np.isnan(speed_values[i]):
            is_immobile[i] = np.nan
    return is_immobile

def calc_interior_zone_polygon(df, bodypart=str, corners=list):
    "Normally, the nose should be used because it indicates the orientation of the mouse best."
    data = df.copy()
    print(f"\nGet time spent of {bodypart} at cage edges...")
    print(f"Filtering {bodypart} for position calculation...")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart+"_likelihood")
    bodypart_x = data[bodypart+"_x"]
    bodypart_y = data[bodypart+"_y"]

    print("Filtering for good corner prediction...")
    
    for corner in corners:
        data = likelihood_filtering(df=data, 
                                    likelihood_row_name=f"{corner}_likelihood",
                                    filter_val=0.99)
    topleft_x = data[f"{corners[0]}_x"]
    topleft_y = data[f"{corners[0]}_y"]
    topright_x = data[f"{corners[1]}_x"]
    topright_y = data[f"{corners[1]}_y"]
    bottomleft_x = data[f"{corners[2]}_x"]
    bottomleft_y = data[f"{corners[2]}_y"]
    bottomright_x = data[f"{corners[3]}_x"]
    bottomright_y = data[f"{corners[3]}_y"]

    bodypart_x = np.array(bodypart_x)
    bodypart_y = np.array(bodypart_y)
    topleft_x = np.array(topleft_x)[0]
    topleft_y = np.array(topleft_y)[0]
    topright_x = np.array(topright_x)[0]
    topright_y = np.array(topright_y)[0]
    bottomleft_x = np.array(bottomleft_x)[0]
    bottomleft_y = np.array(bottomleft_y)[0]
    bottomright_x = np.array(bottomright_x)[0]
    bottomright_y = np.array(bottomright_y)[0]

    #original_corners = [(topleft_x, topleft_y), (topright_x, topright_y), (bottomleft_x,bottomleft_y), (bottomright_x, bottomright_y)]
    scaling_factor = 0.1

    topleft_x += (topright_x - topleft_x) * scaling_factor
    topleft_y += (bottomleft_y - topleft_y) * scaling_factor
    topright_x -= (topright_x - topleft_x) * scaling_factor
    topright_y += (bottomright_y - topright_y) * scaling_factor
    bottomleft_x += (bottomright_x - bottomleft_x) * scaling_factor
    bottomleft_y -= (bottomleft_y - topleft_y) * scaling_factor
    bottomright_x -= (bottomright_x - bottomleft_x) * scaling_factor
    bottomright_y -= (bottomright_y - topright_y) * scaling_factor

    scaled_corners = [(bottomleft_x,bottomleft_y), (bottomright_x, bottomright_y), (topright_x, topright_y), (topleft_x, topleft_y)]

    return (bodypart_x, bodypart_y), scaled_corners

def calc_edge_time(nose_coords=tuple, scaled_corner_coords=list):
    """
    nose_coords should be a tuple of two list containing x and y coordinates, respectively.
    scaled_orner_coords should be a list containing tuples of the scaled corner coordinates
    """
    nose_x = nose_coords[0]
    nose_y = nose_coords[1]
    edge_time = np.zeros(len(nose_x))

    for i in range(len(nose_x)):
        inside = punkt_in_viereck(punkt=(nose_x[i], nose_y[i]), eckpunkte=scaled_corner_coords)
        if not inside:
            edge_time[i] = 1
    return edge_time









