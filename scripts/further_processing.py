import numpy as np
import statistics
import math

def get_paradigm(metadata, parameter_df, left_obj, right_obj):
    if "habituation" in metadata["paradigm"].lower():
        exp_or_hab = "habituation"
    elif "experiment" in metadata["paradigm"].lower():
        exp_or_hab = "experiment"

    if "right" in metadata["paradigm"]:
        try:
            urine_stim = parameter_df[f"is_investigating_{right_obj}"]
            control_stim = parameter_df[f"is_investigating_{left_obj}"]
        except:
            print("No dlc data available.")
        try:
            urine_stim_deg = parameter_df[f"deg_is_investigating_{right_obj}"]
            control_stim_deg = parameter_df[f"deg_is_investigating_{left_obj}"]
        except:
            print("No deg data available.")
        
    elif "left" in metadata["paradigm"]:
        try:
            urine_stim = parameter_df[f"is_investigating_{left_obj}"]
            control_stim = parameter_df[f"is_investigating_{right_obj}"]
        except:
            print("No dlc data available.")
        try:
            urine_stim_deg = parameter_df[f"deg_is_investigating_{left_obj}"]
            control_stim_deg = parameter_df[f"deg_is_investigating_{right_obj}"]
        except:
            print("No deg data available.")
        
    try:
        urine_stim = np.array(urine_stim)
        control_stim = np.array(control_stim)
    except:
        urine_stim = np.zeros(len(parameter_df))
        control_stim = np.zeros(len(parameter_df))
    try:
        urine_stim_deg = np.array(urine_stim_deg)
        control_stim_deg = np.array(control_stim_deg)
    except:
        urine_stim_deg = np.zeros(len(parameter_df))
        control_stim_deg = np.zeros(len(parameter_df))

    return exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg
    
    
def get_behavior_sum(metadata, parameter_df, left_obj, right_obj, dlc=True, deg=True):
    """
    Gets the sum of both investigation behaviors normalized to the experiment duration
    """
    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df, left_obj, right_obj)
    if dlc:
        dlc_calc_stim = np.nansum(urine_stim) / (len(urine_stim)) * 100
        dlc_calc_con = np.nansum(control_stim) / (len(control_stim)) * 100
    else:
        dlc_calc_stim = None
        dlc_calc_con = None
    if deg:
        deg_calc_stim = np.nansum(urine_stim_deg) / (len(urine_stim_deg)) * 100
        deg_calc_con = np.nansum(control_stim_deg) / (len(control_stim_deg)) * 100
    else:
        deg_calc_stim = None
        deg_calc_con = None

    return dlc_calc_stim, dlc_calc_con, deg_calc_stim, deg_calc_con, exp_or_hab


def percent_of_total_inv_time(metadata, parameter_df, left_obj, right_obj, dlc=True, deg=True):

    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df, left_obj, right_obj)
    if dlc:
        dlc_calc = np.nansum(urine_stim) / ((np.nansum(urine_stim) + np.nansum(control_stim))) * 100
    else:
        dlc_calc = None
    if deg:
        deg_calc = np.nansum(urine_stim_deg) / ((np.nansum(urine_stim_deg) + np.nansum(control_stim_deg))) * 100
    else:
        deg_calc = None

    return dlc_calc, deg_calc, exp_or_hab


def disc_index(metadata, parameter_df, left_obj, right_obj, dlc=True, deg=True):

    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df, left_obj, right_obj)
    if dlc:
        dlc_calc = (np.nansum(urine_stim) - np.nansum(control_stim)) / (np.nansum(urine_stim) + np.nansum(control_stim))
    else:
        dlc_calc = None
    if deg:
        deg_calc = (np.nansum(urine_stim_deg) - np.nansum(control_stim_deg)) / (np.nansum(urine_stim_deg) + np.nansum(control_stim_deg))
    else:
        deg_calc = None
    return dlc_calc, deg_calc

def total_inv_time(metadata, parameter_df, left_obj, right_obj, dlc=True, deg=True):
    
    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df, left_obj, right_obj)
    if dlc:
        dlc_calc = (np.nansum(urine_stim) + np.nansum(control_stim)) / np.count_nonzero(~np.isnan(urine_stim)) * 100
    else:
        dlc_calc = None
    if deg:
        deg_calc = (np.nansum(urine_stim_deg) + np.nansum(control_stim_deg)) / np.count_nonzero(~np.isnan(urine_stim_deg)) * 100
    else: 
        deg_calc = None
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
    distance_travelled = parameter_df["distance_travelled_center_in_m"]
    distance_travelled = np.array(distance_travelled)
    distance = np.nansum(distance_travelled)/np.count_nonzero(~np.isnan(distance_travelled)) * 3600
    return distance

def full_immobile_time(parameter_df):
    """
    Return the % of time the mouse was immobile during the recording.
    """
    immobile_time = parameter_df["is_immobile"]
    immobile_time = np.array(immobile_time)
    immobile_time = np.nansum(immobile_time)/np.count_nonzero(~np.isnan(immobile_time)) * 100
    return immobile_time

def analyze_ethogram(metadata, parameter_df, left_obj, right_obj, dlc_or_deg = "deg", control_or_stim = "stim"):

    exp_or_hab, urine_stim, control_stim, urine_stim_deg, control_stim_deg = get_paradigm(metadata, parameter_df, left_obj, right_obj)

    if dlc_or_deg == "deg":
        if control_or_stim == "stim": 
            arr = urine_stim_deg
        else:
            arr = control_stim_deg
    else:
        if control_or_stim == "stim":
            arr = urine_stim
        else:
            arr = control_stim

    event_count = 0
    bout_lengths = []
    current_bout_length = 0
    in_bout = False
    
    for i in range(len(arr)):
        if arr[i] == 1:
            if not in_bout:
                in_bout = True
                event_count += 1
            current_bout_length += 1
        else:
            if in_bout:
                in_bout = False
                bout_lengths.append(current_bout_length)
                current_bout_length = 0
    
    # Append the last bout if it ends at the end of the array
    if in_bout:
        bout_lengths.append(current_bout_length)
    
    try:

        if bout_lengths:
            # Calculate the average bout length
            average_bout_length = sum(bout_lengths) / len(bout_lengths)
            # Calculate standard deviation
            sd_bout_length = statistics.stdev(bout_lengths)
            # Calculate standard error of the mean
            sem_bout_length = sd_bout_length / math.sqrt(len(bout_lengths))
        else:
            average_bout_length = 0
            sd_bout_length = 0
            sem_bout_length = 0

    except:
        print("Error during average/sem/sd bot length calculation")
        average_bout_length = 0
        sd_bout_length = 0
        sem_bout_length = 0
    
    return event_count, average_bout_length, sd_bout_length, sem_bout_length






