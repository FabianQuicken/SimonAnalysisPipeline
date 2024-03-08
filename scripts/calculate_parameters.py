import numpy as np
import pandas as pd
from mathematics import euklidean_distance
from likelihood_filter import likelihood_filtering,likelihood_filtering_nans

pixel_per_cm=34.77406

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
                                filter_val=0.99)
    data = likelihood_filtering(df=data, 
                                likelihood_row_name=edge_right+"_likelihood",
                                filter_val=0.99)
    edge_left_x = data[edge_left+"_x"]
    edge_right_x = data[edge_right+"_x"]

    bodypart_x = np.array(bodypart_x)
    edge_left_x = np.array(edge_left_x)
    edge_right_x = np.array(edge_right_x)
    edge_left_x = edge_left_x[0]
    edge_right_x = edge_right_x[0]
    

    middle = (edge_left_x + edge_right_x) / 2
    print(f"The edges (left,right) are set as {round(edge_left_x)}, {round(edge_right_x)}. The midpoint is {round(middle)}.")
    
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

    return is_left_values,is_right_values






def distance_travelled(df,bodypart=str):
    """
    Takes a Dataframe and a bodypart as input
    calculates the distance of a keypoint
    between consequetive frames in cm.
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
        distance_values[i] = distance_values[i] / pixel_per_cm
    return distance_values



def calculate_speed(distance_array,fps=60):
    """
    calculates the speed between frames in km/h
    """
    print("\nGet speed values...")
    #distance_values = np.array(parameter_df["distance"])
    distance_values = distance_array
    for i in range(len(distance_values)):
        distance_values[i]=((distance_values[i]*fps))*0.036 #changing cm/s to km/h
    speed_between_frames = distance_values
    for i in range(len(speed_between_frames)-1):
        if speed_between_frames[i] > 50:
            speed_between_frames[i] = np.nan
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

    print("Filtering for a good object prediction...")
    data = likelihood_filtering(df=data, 
                                likelihood_row_name=object+"_likelihood",
                                filter_val=0.99)
    object_x = data[object+"_x"]
    object_y = data[object+"_y"]


    bodypart_x = np.array(bodypart_x)
    bodypart_y = np.array(bodypart_y)
    object_x = np.array(object_x)
    object_y = np.array(object_y)
    object_x = object_x[0]
    object_y = object_y[0]


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
    pixel_per_cm = 34.77406
    radius_threshold = factor * pixel_per_cm
    is_investigating = np.zeros((len(distance_values)))
    for i in range(len(distance_values)-1):
        if distance_values[i] < radius_threshold:
            is_investigating[i] = 1
    return is_investigating, factor

def immobile_time(speed_values, immobile_threshold = 0.1):
    print("\nGet immobile time...")
    is_immobile = np.zeros((len(speed_values)))
    for i in range(len(speed_values)-1):
        if speed_values[i] < immobile_threshold:
            is_immobile[i] = 1
    return is_immobile, immobile_threshold







