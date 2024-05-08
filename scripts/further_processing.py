import numpy as np
import statistics

def get_paradigm(metadata, parameter_df, left_obj, right_obj):
    if "habituation" in metadata["paradigm"].lower():
        exp_or_hab = "habituation"
    elif "experiment" in metadata["paradigm"].lower():
        exp_or_hab = "experiment"

    if "right" in metadata["paradigm"]:
        urine_stim = parameter_df[f"is_investigating_{right_obj}"]
        control_stim = parameter_df[f"is_investigating_{left_obj}"]
        try:
            urine_stim_deg = parameter_df[f"deg_is_investigating_{right_obj}"]
            control_stim_deg = parameter_df[f"deg_is_investigating_{left_obj}"]
        except:
            print("No deg data available.")
        
    elif "left" in metadata["paradigm"]:
        urine_stim = parameter_df[f"is_investigating_{left_obj}"]
        control_stim = parameter_df[f"is_investigating_{right_obj}"]
        try:
            urine_stim_deg = parameter_df[f"deg_is_investigating_{left_obj}"]
            control_stim_deg = parameter_df[f"deg_is_investigating_{right_obj}"]
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





