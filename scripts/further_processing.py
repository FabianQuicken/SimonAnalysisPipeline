def get_paradigm(metadata, parameter_df):
    if "habituation" in metadata["paradigm"].lower():
        exp_or_hab = "habituation"
    elif "experiment" in metadata["paradigm"].lower():
        exp_or_hab = "experiment"
    if "dish" in metadata["paradigm"]:
        if "right" in metadata["paradigm"]:
            urine_stim = parameter_df["is_investigating_rightdish"]
            control_stim = parameter_df["is_investigating_leftdish"]
        elif "left" in metadata["paradigm"]:
            urine_stim = parameter_df["is_investigating_leftdish"]
            control_stim = parameter_df["is_investigating_rightdish"]
    
    return exp_or_hab, urine_stim, control_stim
    
    



def percent_of_total_inv_time(metadata, parameter_df):

    exp_or_hab, urine_stim, control_stim = get_paradigm(metadata, parameter_df)
    return sum(urine_stim) / ((sum(urine_stim) + sum(control_stim))) * 100, exp_or_hab


def disc_index(metadata, parameter_df):

    exp_or_hab, urine_stim, control_stim = get_paradigm(metadata, parameter_df)
    return (sum(urine_stim) - sum(control_stim)) / (sum(urine_stim) + sum(control_stim)), exp_or_hab

def total_inv_time(metadata, parameter_df):
    
    exp_or_hab, urine_stim, control_stim = get_paradigm(metadata, parameter_df)
    return sum(urine_stim) + sum(control_stim), exp_or_hab

