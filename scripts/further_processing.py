import numpy as np
import statistics

def get_paradigm(metadata, parameter_df):
    if "habituation" in metadata["paradigm"].lower():
        exp_or_hab = "habituation"
    elif "experiment" in metadata["paradigm"].lower():
        exp_or_hab = "experiment"

    if "right" in metadata["paradigm"]:
        urine_stim = parameter_df["is_investigating_rightdish"]
        control_stim = parameter_df["is_investigating_leftdish"]
        print("right")
    elif "left" in metadata["paradigm"]:
        urine_stim = parameter_df["is_investigating_leftdish"]
        control_stim = parameter_df["is_investigating_rightdish"]
        print("left")

    urine_stim = np.array(urine_stim)
    control_stim = np.array(control_stim)

    return exp_or_hab, urine_stim, control_stim
    
    



def percent_of_total_inv_time(metadata, parameter_df):

    exp_or_hab, urine_stim, control_stim = get_paradigm(metadata, parameter_df)
    return sum(urine_stim) / ((sum(urine_stim) + sum(control_stim))) * 100, exp_or_hab


def disc_index(metadata, parameter_df):

    exp_or_hab, urine_stim, control_stim = get_paradigm(metadata, parameter_df)
    return (sum(urine_stim) - sum(control_stim)) / (sum(urine_stim) + sum(control_stim))

def total_inv_time(metadata, parameter_df):
    
    exp_or_hab, urine_stim, control_stim = get_paradigm(metadata, parameter_df)
    return sum(urine_stim) + sum(control_stim) / len(urine_stim) * 100

def median_speed(parameter_df):
    median_speed = parameter_df["speed_in_km/h"]
    median_speed = np.array(median_speed)
    median_speed = np.nanmedian(median_speed)
    return median_speed

def full_distance(parameter_df):
    """
    returns the distance travelled per minute
    """
    distance_travelled = parameter_df["distance_travelled_center"]
    distance_travelled = np.array(distance_travelled)
    distance = np.nansum(distance_travelled)/len(distance_travelled) * 36000 / 100
    return distance

def full_immobile_time(parameter_df):
    """
    Return the % of time the mouse was immobile during the recording.
    """
    immobile_time = parameter_df["is_immobile"]
    immobile_time = np.array(immobile_time)
    immobile_time = np.nansum(immobile_time)/len(immobile_time) * 100
    return immobile_time





