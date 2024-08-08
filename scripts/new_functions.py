

def where_is_the_stimulus(metadata, experiment=None):

    stimulus_side = ''
    paradigm = metadata["paradigm"]
    paradigm_list = paradigm.split('_')

    # get the paradigm part that contains the left right information:
    # First Simons und mein normal 2 petridish paradigm
    if experiment is None:
        #meins
        if metadata["camera"] == "topview":
            important_paradigm_part = 0
        #simons
        else:
            important_paradigm_part = 2
    # Simons paired urine experiment
    elif experiment == "vol_vs_invol":
        important_paradigm_part = 1
    # Frizis sick/healthy experiment
    elif experiment == "sick_vs_healthy":
        important_paradigm_part = 3

    if "right" in paradigm_list[important_paradigm_part]:
        stimulus_side = "right"
    elif "left" in paradigm_list[important_paradigm_part]:
        stimulus_side = "left"
    
    # der interessante stimulus für frizi ist sick
    elif "sick" in paradigm_list[important_paradigm_part]:
        stimulus_side = "left"
    elif "healthy" in paradigm_list[important_paradigm_part]:
        stimulus_side = "right"
    elif "clean" in paradigm_list[important_paradigm_part]:
        stimulus_side = None
    else:
        print(f"Warning: No Stimulus side found in {paradigm_list[2]} The paradigm is: {paradigm}.")
    
    return stimulus_side


def what_is_the_cohort(metadata, experiment=None):

    cohort = ''
    paradigm = metadata["paradigm"]
    paradigm_list = paradigm.split('_')

    # erstmal simons und meine cohorte
    if experiment is None:
        # meins und simons
        cohort = paradigm_list[1]
    
    # simons gepaartes experiment
    if experiment == "vol_vs_invol":
        cohort = paradigm_list[2] + "_" + paradigm_list[3]

    # simons experiment
    if experiment == "sick_vs_healthy":
        cohort == paradigm_list[0] + "_" + paradigm[1][0:3] + "_" + paradigm[2] 

    return cohort


        

