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
        try:
            urine_stim_deg = parameter_df["deg_is_investigating_rightdish"]
            control_stim_deg = parameter_df["deg_is_investigating_leftdish"]
        except:
            print("No deg data available.")
        
    elif "left" in metadata["paradigm"]:
        urine_stim = parameter_df["is_investigating_leftdish"]
        control_stim = parameter_df["is_investigating_rightdish"]
        try:
            urine_stim_deg = parameter_df["deg_is_investigating_leftdish"]
            control_stim_deg = parameter_df["deg_is_investigating_rightdish"]
        except:
            print("No deg data available.")
        

    urine_stim = np.array(urine_stim)
    control_stim = np.array(control_stim)
    try:
        urine_stim_deg = np.array(urine_stim_deg)
        control_stim_deg = np.array(control_stim_deg)
    except:
        urine_stim_deg = np.zeros(len(urine_stim))
        control_stim_deg = np.zeros(len(control_stim))

    return exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg
    
    



def percent_of_total_inv_time(metadata, parameter_df):

    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df)
    dlc_calc = sum(urine_stim) / ((sum(urine_stim) + sum(control_stim))) * 100
    deg_calc = sum(urine_stim_deg) / ((sum(urine_stim_deg) + sum(control_stim_deg))) * 100
    return dlc_calc, deg_calc, exp_or_hab


def disc_index(metadata, parameter_df):

    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df)
    dlc_calc = (sum(urine_stim) - sum(control_stim)) / (sum(urine_stim) + sum(control_stim))
    deg_calc = (sum(urine_stim_deg) - sum(control_stim_deg)) / (sum(urine_stim_deg) + sum(control_stim_deg))
    return dlc_calc, deg_calc

def total_inv_time(metadata, parameter_df):
    
    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df)
    dlc_calc = (sum(urine_stim) + sum(control_stim)) / len(urine_stim) * 100
    deg_calc = (sum(urine_stim_deg) + sum(control_stim_deg)) / len(urine_stim_deg) * 100
    return dlc_calc, deg_calc

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





