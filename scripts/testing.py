import glob
from tqdm import tqdm
import time
import pandas as pd
import numpy as np
import shutil
import os
import matplotlib.pyplot as plt
import seaborn as sns

from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv, ini_processed_parameters_df, append_processed_parameters_df, save_hab_exp
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object,time_spent_sides,investigation_time,immobile_time, calc_interior_zone_polygon, calc_edge_time
from further_processing import percent_of_total_inv_time, disc_index, total_inv_time, median_speed, full_distance, full_immobile_time, analyze_ethogram, get_behavior_sum, total_cage_edge_time
from get_parameters import find_parameter_file
from configurations import dlc_petridish_layout_fabi, dlc_petridish_layout_simon, dlc_mighty_snicket_layout_simon,dlc_petridish_layout_frizi
from split_exp_hab import split_csv, split_csv_chatgpt
from figures import eventplot, pieplot, plot_cum_dist, plot_distance_val, prepare_data_line_plot, plot_multiple_line_plots, plot_multiple_line_plots_chatgpt
from calculate_dish_center import calc_coordinate_center, get_high_likelihood_dish_coordinates, add_dish_center_to_bodypart_df
from cut_frizi_df_to_experiment_length import find_first_frame_with_mouse, cut_bodypart_df_to_experiment_timerange
#from move_file import move_file

# # # # !!! EDIT THE CODE ONLY HERE !!! # # # # 
# # # # Define your experiment here # # # #

# define the project path - head directory of your specific dataset, that should be analyzed similarly
project_path = "./datasets/FS_petridishes_sick_healthy"

# if there is a specific naming convention, code needs to be passed to the get_metadata()
# basic convention is: "date_camera_mouse_paradigm_paradigm_paradigm"
# right now, "vol_vs_invol" is an extra option - use None for others!
# further extra option: "sick_vs_healthy"
exp_meta_code = "sick_vs_healthy"

# how are your objects named?
left_obj = "left_dish"
right_obj = "right_dish"

# do you want to process dlc csv files?
dlc_analysis = True
if dlc_analysis:

    # # # Important # # #
    # go to configurations.py and change the pixel_per_cm if needed !!
    # # # Important # # # 

    # the dlc layout contains information about the column names of the bodyparts
    dlc_layout = dlc_petridish_layout_frizi
    

    # define the bodyparts you want to extract out of the df for further calculations
    used_bodyparts = ["snout",
                      "centroid",
                      "leftpetrileft",
                      "leftpetriright",
                      "leftpetritop",
                      "leftpetribottom",
                      "rightpetrileft",
                      "rightpetriright",
                      "rightpetritop",
                      "rightpetribottom", 
                      "cagetopleft",
                      "cagetopright",
                      "cagebottomleft",
                      "cagebottomright"]
    
    # if you turn this on, the code will find the first frame with a mouse predicted
    cut_df_to_mouse_presence = True
    # frizis experiments take 10 minutes after putting the mouse in the cage
    # she has 20 fps, therefore the experiment ends after 12.000 datapoints
    # if set to None, the data will be cut from mouse presence to recording end
    df_second_cut = 12000
    # this is the DLC label that will be searched for presence
    label_to_search_for = "centroid"

    # do you need to calculate the dish center because you labelled four dish edges? 
    calc_dish_center = True


    calc_distance_and_speed = True
    # what bodypart do you want to use for distance and speed calculation?
    distance_bodypart = "centroid"

    calc_immobile_time = True
    # below what speed threshold [km/h] the animal is defined immobile?
    immobile_threshold = 0.1

    calc_cage_edge_time = True
    # what bodypart should be checked for being close at the edges?
    edge_bodypart = "snout"
    # how are the cage corners named? 
    # syntax needs to be: topleft, topright, bottomleft, bottomright
    corners = ["cagetopleft", "cagetopright", "cagebottomleft", "cagebottomright"]


    calc_dist_left_object = True
    calc_dist_right_object = True
    # what bodypart and object are used for distance calculation?
    obj_dist_bodypart = "snout"
    left_obj = left_obj
    right_obj = right_obj
    # do you want to calculate investigation behavior based on the distance?
    calc_inv_time = True
    # What is the distance in cm, from where it should be counted as investigation?
    # e.g. frizis petridishes have a 6 cm diameter, therefore a radius of 3 cm should be chosen
    investigation_distance_thresh = 3 # this will be multiplied with pixel_per_cm from configurations.py

    calc_side_pref = True
    # give the bodypart that is checked for sidepref
    side_pref_bodypart = "centroid"
    # give two coordinates that define the edges of the arena
    # will be used to 'draw' a center line 
    left_edge = "cagetopleft"
    right_edge = "cagetopright"

    # do you want to save the used bodyparts in an extra csv?
    save_bodyparts = True
    # do you want to save the calculated parameters to a csv?
    save_parameters = True

    # do you want to move the raw dlc csv's from 'new' to 'done' folder?
    move_raw_csv = False

# do you want to do postprocessing?
run_postprocessing = False
if run_postprocessing:
    # do you want to calculate the total time in % of each behavior?
    analyze_sum_behavior = True
    # do you want to calculate the amount of stimulus investigation to total investigation (stim + water)?
    analyze_stim_inv_to_total = True
    # do you want to calculate the total investigation time (both dishes together)
    analyze_total_inv = True
    # do you wnt to calculate the discrimination index towards the stimulus side?
    analyze_discrimination = True
    # do you want to analyze behavior predictions for bout count and bout length?
    analyze_bouts = True
    if analyze_bouts:
        # for deg?
        analyze_deg_stim_bouts = True
        # for deg control investigation? (default is stimulus investigation)
        analyze_deg_con_bouts = True
        # for dlc?
        analyze_dlc_stim_bouts = True
        # for dlc control investigation?
        analyze_dlc_con_bouts = True
        # for asoid?
        analyze_asoid_stim_bouts = True
        # for asoid control investigation?
        analyze_asoid_con_bouts = True
    # do you want to analyze movement behavior? (median speed, distance travelled and immobile time)
    analyze_movement = True
    # should the parameter file be moved in the 'done' directory?
    move_para_file = True



# for 20min videos: split csv files in habituation and experiment files...
cut_dlc = False
cut_deg = False
if cut_dlc:
    # get path of all files
    path = f"{project_path}/raw/dlc_new/"
    # get only .csv files
    file_list = glob.glob(os.path.join(path, '*.csv'))

    for file in tqdm(file_list):
        time.sleep(0.2)
        split_csv_chatgpt(input_file=file, output_path=path, dlc=True)

if cut_deg:
    deg_path = f"{project_path}/raw/deg_new/*.csv"
    deg_file_list = glob.glob(deg_path)

    deg_output_path = f"{project_path}/raw/deg_new/"

    for deg_file in tqdm(deg_file_list):
        time.sleep(0.2)
        split_csv_chatgpt(input_file=deg_file, output_path=deg_output_path, deg=True)

# # # # Define your experiment here # # # #
# # # # !!! EDIT THE CODE ONLY HERE !!! # # # # 



# # # # Start: Get data from DeepLabCut, calculate parameters, save used bodyparts and parameters as csv  # # # #

if dlc_analysis:
    # get path of all files
    path = f"{project_path}/raw/dlc_new/"
    path_done = f"{project_path}/raw/dlc_done/"
    # get only .csv files
    file_list = glob.glob(os.path.join(path, '*.csv'))




    # calculate basic parametersfrom dlc data
    for file in tqdm(file_list):
        print(f"Working on file: {file}")
        time.sleep(0.2)

        df = rewrite_dataframe(csv_file_path=file, df_cols=dlc_layout) # rewrites the dataframe of dlc for easier readibility
        metadata = get_metadata(csv_file_path=file, experiment=exp_meta_code) # get metadata from the file name
        # new df only containing bodypart data used for calculations

        new_df = get_bodypart(df_all_bp=df,bodypart_list=used_bodyparts)

        
        # calculates the dish centers and add them to the bodypart df
        if calc_dish_center:
            left_dish_x_coords, left_dish_y_coords = get_high_likelihood_dish_coordinates(df, 
                                                                                        object_edge_names = ["leftpetrileft",
                                                                                                            "leftpetriright",
                                                                                                            "leftpetritop",
                                                                                                            "leftpetribottom"
                                                                                                            ], 
                                                                                        thresh = 0.99)
            right_dish_x_coords, right_dish_y_coords = get_high_likelihood_dish_coordinates(df, 
                                                                                        object_edge_names = ["rightpetrileft",
                                                                                                            "rightpetriright",
                                                                                                            "rightpetritop",
                                                                                                            "rightpetribottom"
                                                                                                            ], 
                                                                                        thresh = 0.99)

            left_dish_center_x_coord, left_dish_center_y_coord = calc_coordinate_center(x_coords_list=left_dish_x_coords,
                                                                                        y_coords_list=left_dish_y_coords)

            right_dish_center_x_coord, right_dish_center_y_coord = calc_coordinate_center(x_coords_list=right_dish_x_coords,
                                                                                        y_coords_list=right_dish_y_coords)
            
            add_dish_center_to_bodypart_df(bodypart_df=new_df,
                                           dish_center_x=left_dish_center_x_coord,
                                           dish_center_y=left_dish_center_y_coord,
                                           column_name="left_dish")
            
            add_dish_center_to_bodypart_df(bodypart_df=new_df,
                                           dish_center_x=right_dish_center_x_coord,
                                           dish_center_y=right_dish_center_y_coord,
                                           column_name="right_dish")
            
        if cut_df_to_mouse_presence:
            df_first_cut = find_first_frame_with_mouse(bodypart_df=new_df,
                                                       label_to_search_for=label_to_search_for)
            
            new_df = cut_bodypart_df_to_experiment_timerange(bodypart_df=new_df,
                                                             first_cut_point=df_first_cut,
                                                             second_cut_point=df_second_cut)
            

            
        parameters = {}
        
        # getting all the parameters from the DLC Data
        if calc_distance_and_speed:
            distance = distance_travelled(df = new_df, bodypart = distance_bodypart)
            speed = calculate_speed(distance)
            parameters["distance_travelled_center_in_m"] = distance
            parameters["speed_in_km/h"] = speed

        if calc_immobile_time:
            is_immobile = immobile_time(speed_values=speed, immobile_threshold=immobile_threshold)
            # adding array containing information about the speed threshold for immobile behavior
            immobile_speeds = np.zeros(len(is_immobile))
            for i in range(len(immobile_speeds)-1):
                immobile_speeds[i] = immobile_threshold
            parameters["is_immobile"] = is_immobile
            parameters["immobile_threshold[km/h]"] = immobile_speeds

        if calc_cage_edge_time:
            nose_coords, scaled_corner_coords = calc_interior_zone_polygon(df=new_df, bodypart=edge_bodypart, corners=corners)
            edge_time = calc_edge_time(nose_coords, scaled_corner_coords)
            parameters[f"is close to edge"] = edge_time

        if calc_dist_left_object:
            distance_to_left_object = distance_bodypart_object(df=new_df,bodypart=obj_dist_bodypart,object=left_obj)
            parameters[f"distance_nose_{left_obj}"] = distance_to_left_object

        if calc_dist_right_object:
            distance_to_right_object = distance_bodypart_object(df=new_df,bodypart=obj_dist_bodypart,object=right_obj)
            parameters[f"distance_nose_{right_obj}"] = distance_to_right_object

        if calc_side_pref:
            is_left, is_right = time_spent_sides(df = new_df,bodypart=side_pref_bodypart,edge_left=left_edge, edge_right=right_edge)
            parameters["center_is_left_cagehalf"] = is_left
            parameters["center_is_right_cagehalf"] = is_right

        if calc_inv_time:
            print("\nGet dish investigation left...")
            is_investigating_left, factor = investigation_time(distance_to_left_object,factor=investigation_distance_thresh)
            print("\nGet dish investigation right...")
            is_investigating_right, factor = investigation_time(distance_to_right_object,factor=investigation_distance_thresh)
            # adding array containing information about the radius used for petridish investigation 
            radius_petridish = np.zeros(len(is_investigating_left))
            for i in range(len(radius_petridish)-1):
                radius_petridish[i] = factor
            parameters[f"dlc_is_investigating_{left_obj}"] = is_investigating_left
            parameters[f"dlc_is_investigating_{right_obj}"] = is_investigating_right
            parameters["object_investigation_radius[cm]"] = radius_petridish


        # bodyparts for calculations & parameters get saved to new csv's, respectively
        if save_bodyparts:
            metadata_bodyparts_to_csv(metadata_dic=metadata,bodyparts_df=new_df,path=f"{project_path}/processed/bodyparts/")
        if save_parameters:
            parameters_to_csv(metadata_dic=metadata,parameters=parameters,path=f"{project_path}/processed/parameters/new/")

        # dlc file goes to the respective 'done' folder
        if move_raw_csv:
            shutil.move(file, path_done)

# # # # End: Get data from DeepLabCut, calculate parameters, save used bodyparts and parameters as csv  # # # #


# # # # Start: Take processed (parameter) data, calculate metrics, save metrics of similar paradigm recordings in one csv  # # # #
if run_postprocessing:
    # set paths and get parameter data
    path_parameters = f"{project_path}/processed/parameters/new/*.csv"
    path_parameters_done = f"{project_path}/processed/parameters/done/"
    file_list_parameters = glob.glob(path_parameters)

    # since we loop over multiple files and save everything into one file, we need one dataframe where all data is stored
    # therefore, we first need to initialize the df, then append to it
    # this variable checks, if a df was initialized and is first set to False
    p_parameters_df_initialized = False
    #p_parameters_df = pd.DataFrame()
    p_parameters = {}

    for file in tqdm(file_list_parameters):
        print(f"Working on file: {file}")
        time.sleep(0.2)

        if p_parameters_df_initialized:
            p_parameters = []

        metadata = get_metadata(csv_file_path=file,experiment=exp_meta_code)
        parameters_df = pd.read_csv(file)
        
        if analyze_sum_behavior:
            dlc_calc_stim, dlc_calc_con, deg_calc_stim, deg_calc_con, asoid_calc_stim, asoid_calc_con, exp_or_hab = get_behavior_sum(metadata,
                                                                                                    parameters_df,
                                                                                                    left_obj=left_obj,
                                                                                                    right_obj=right_obj)
            if not p_parameters_df_initialized:
                p_parameters["Stimulus investigation DLC [%]"] = dlc_calc_stim
                p_parameters["Stimulus investigation DEG [%]"] = deg_calc_stim
                p_parameters["Stimulus investigation Asoid [%]"] = asoid_calc_stim
                p_parameters["Control investigation DLC [%]"] = dlc_calc_con
                p_parameters["Control investigation DEG [%]"] = deg_calc_con
                p_parameters["Control investigation Asoid [%]"] = asoid_calc_con
                
            elif p_parameters_df_initialized:
                p_parameters.append(dlc_calc_stim)
                p_parameters.append(deg_calc_stim)
                p_parameters.append(asoid_calc_con)
                p_parameters.append(dlc_calc_con)
                p_parameters.append(deg_calc_con)
                p_parameters.append(asoid_calc_con)

        if analyze_stim_inv_to_total:
            perc_total_inv_dlc, perc_total_inv_deg, perc_total_inv_asoid, exp_or_hab = percent_of_total_inv_time(metadata,parameters_df, left_obj=left_obj, right_obj=right_obj)       
            if not p_parameters_df_initialized:
                p_parameters["Stimulus to total investigation DLC [%]"] = perc_total_inv_dlc
                p_parameters["Stimulus to total investigation DEG [%]"] = perc_total_inv_deg
                p_parameters["Stimulus to total investigation Asoid [%]"] = perc_total_inv_asoid
            elif p_parameters_df_initialized:
                    p_parameters.append(perc_total_inv_dlc)
                    p_parameters.append(perc_total_inv_deg)
                    p_parameters.append(perc_total_inv_asoid) 
                           
        if analyze_total_inv:
            total_inv_dlc, total_inv_deg, total_inv_asoid = total_inv_time(metadata, parameters_df, left_obj=left_obj, right_obj=right_obj)
            if not p_parameters_df_initialized:
                p_parameters["Total investigation time DLC [%]"] = total_inv_dlc
                p_parameters["Total investigation time DEG [%]"] = total_inv_deg
                p_parameters["Total investigation time Asoid [%]"] = total_inv_asoid
            elif p_parameters_df_initialized:
                    p_parameters.append(total_inv_dlc)
                    p_parameters.append(total_inv_deg)
                    p_parameters.append(total_inv_asoid)
        
        if analyze_discrimination:
            disc_ind_dlc, disc_ind_deg, disc_ind_asoid = disc_index(metadata, parameters_df, left_obj=left_obj, right_obj=right_obj)
            if not p_parameters_df_initialized:
                p_parameters["Discrimination Index DLC"] = disc_ind_dlc
                p_parameters["Discrimination Index DEG"] = disc_ind_deg
                p_parameters["Discrimination Index Asoid"] = disc_ind_asoid
            elif p_parameters_df_initialized:
                    p_parameters.append(disc_ind_dlc)
                    p_parameters.append(disc_ind_deg)
                    p_parameters.append(disc_ind_asoid)
        
        if analyze_bouts:
            if analyze_deg_stim_bouts:
                deg_stim_event_count, deg_stim_average_bout_length, deg_stim_sd_bout_length, deg_stim_sem_bout_length = analyze_ethogram(metadata,
                                                                                                                                         parameters_df,
                                                                                                                                         left_obj=left_obj,
                                                                                                                                         right_obj=right_obj,
                                                                                                                                         dlc_or_deg="deg",
                                                                                                                                         control_or_stim="stim")
                if not p_parameters_df_initialized:
                    p_parameters["Stimulus investigation events DEG"] = deg_stim_event_count
                    p_parameters["Stimulus investigation average bout length DEG"] = deg_stim_average_bout_length
                    p_parameters["Stimulus investigation SD bout length DEG"] = deg_stim_sd_bout_length
                    p_parameters["Stimulus investigation SEM bout length DEG"] = deg_stim_sem_bout_length
                elif p_parameters_df_initialized:
                    p_parameters.append(deg_stim_event_count)
                    p_parameters.append(deg_stim_average_bout_length)
                    p_parameters.append(deg_stim_sd_bout_length)
                    p_parameters.append(deg_stim_sem_bout_length)

            if analyze_deg_con_bouts:
                deg_con_event_count, deg_con_average_bout_length, deg_con_sd_bout_length, deg_con_sem_bout_length = analyze_ethogram(metadata,
                                                                                                                                     parameters_df,
                                                                                                                                     left_obj=left_obj,
                                                                                                                                     right_obj=right_obj,
                                                                                                                                     dlc_or_deg="deg",
                                                                                                                                     control_or_stim="con")
                if not p_parameters_df_initialized:
                    p_parameters["Water investigation events DEG"] = deg_con_event_count
                    p_parameters["Water investigation average bout length DEG"] = deg_con_average_bout_length
                    p_parameters["Water investigation SD bout length DEG"] = deg_con_sd_bout_length
                    p_parameters["Water investigation SEM bout length DEG"] = deg_con_sem_bout_length
                elif p_parameters_df_initialized:
                    p_parameters.append(deg_con_event_count)
                    p_parameters.append(deg_con_average_bout_length)
                    p_parameters.append(deg_con_sd_bout_length)
                    p_parameters.append(deg_con_sem_bout_length)
            
            if analyze_dlc_stim_bouts:
                dlc_stim_event_count, dlc_stim_average_bout_length, dlc_stim_sd_bout_length, dlc_stim_sem_bout_length = analyze_ethogram(metadata,
                                                                                                                                         parameters_df,
                                                                                                                                         left_obj=left_obj,
                                                                                                                                         right_obj=right_obj,
                                                                                                                                         dlc_or_deg="dlc", 
                                                                                                                                         control_or_stim="stim")
                if not p_parameters_df_initialized:
                    p_parameters["Stimulus investigation events DLC"] = dlc_stim_event_count
                    p_parameters["Stimulus investigation average bout length DLC"] = dlc_stim_average_bout_length
                    p_parameters["Stimulus investigation SD bout length DLC"] = dlc_stim_sd_bout_length
                    p_parameters["Stimulus investigation SEM bout length DLC"] = dlc_stim_sem_bout_length
                elif p_parameters_df_initialized:
                    p_parameters.append(dlc_stim_event_count)
                    p_parameters.append(dlc_stim_average_bout_length)
                    p_parameters.append(dlc_stim_sd_bout_length)
                    p_parameters.append(dlc_stim_sem_bout_length)

            if analyze_dlc_con_bouts:
                dlc_con_event_count, dlc_con_average_bout_length, dlc_con_sd_bout_length, dlc_con_sem_bout_length = analyze_ethogram(metadata, 
                                                                                                                                     parameters_df,
                                                                                                                                     left_obj=left_obj,
                                                                                                                                     right_obj=right_obj,
                                                                                                                                     dlc_or_deg="dlc",
                                                                                                                                     control_or_stim="con")
                if not p_parameters_df_initialized:
                    p_parameters["Water investigation events DLC"] = dlc_con_event_count
                    p_parameters["Water investigation average bout length DLC"] = dlc_con_average_bout_length
                    p_parameters["Water investigation SD bout length DLC"] = dlc_con_sd_bout_length
                    p_parameters["Water investigation SEM bout length DLC"] = dlc_con_sem_bout_length
                elif p_parameters_df_initialized:
                    p_parameters.append(dlc_con_event_count)
                    p_parameters.append(dlc_con_average_bout_length)
                    p_parameters.append(dlc_con_sd_bout_length)
                    p_parameters.append(dlc_con_sem_bout_length)


            if analyze_asoid_stim_bouts:
                asoid_stim_event_count, asoid_stim_average_bout_length, asoid_stim_sd_bout_length, asoid_stim_sem_bout_length = analyze_ethogram(metadata,
                                                                                                                                         parameters_df,
                                                                                                                                         left_obj=left_obj,
                                                                                                                                         right_obj=right_obj,
                                                                                                                                         dlc_or_deg="asoid", 
                                                                                                                                         control_or_stim="stim")
                if not p_parameters_df_initialized:
                    p_parameters["Stimulus investigation events Asoid"] = asoid_stim_event_count
                    p_parameters["Stimulus investigation average bout length Asoid"] = asoid_stim_average_bout_length
                    p_parameters["Stimulus investigation SD bout length Asoid"] = asoid_stim_sd_bout_length
                    p_parameters["Stimulus investigation SEM bout length Asoid"] = asoid_stim_sem_bout_length
                elif p_parameters_df_initialized:
                    p_parameters.append(asoid_stim_event_count)
                    p_parameters.append(asoid_stim_average_bout_length)
                    p_parameters.append(asoid_stim_sd_bout_length)
                    p_parameters.append(asoid_stim_sem_bout_length)

            if analyze_asoid_con_bouts:
                asoid_con_event_count, asoid_con_average_bout_length, asoid_con_sd_bout_length, asoid_con_sem_bout_length = analyze_ethogram(metadata, 
                                                                                                                                     parameters_df,
                                                                                                                                     left_obj=left_obj,
                                                                                                                                     right_obj=right_obj,
                                                                                                                                     dlc_or_deg="asoid",
                                                                                                                                     control_or_stim="con")
                if not p_parameters_df_initialized:
                    p_parameters["Water investigation events Asoid"] = asoid_con_event_count
                    p_parameters["Water investigation average bout length Asoid"] = asoid_con_average_bout_length
                    p_parameters["Water investigation SD bout length Asoid"] = asoid_con_sd_bout_length
                    p_parameters["Water investigation SEM bout length Asoid"] = asoid_con_sem_bout_length
                elif p_parameters_df_initialized:
                    p_parameters.append(asoid_con_event_count)
                    p_parameters.append(asoid_con_average_bout_length)
                    p_parameters.append(asoid_con_sd_bout_length)
                    p_parameters.append(asoid_con_sem_bout_length)
                
        if analyze_movement:

            median_speed_val = median_speed(parameters_df)
            distance_per_min = full_distance(parameters_df)
            immobile_percentage = full_immobile_time(parameters_df)
            cage_edge_time_percentage = total_cage_edge_time(parameters_df)

            if not p_parameters_df_initialized:
                p_parameters["Median speed [km/h]"] = median_speed_val
                p_parameters["Distance per minute [m]"] = distance_per_min
                p_parameters["Immobile time [%]"] = immobile_percentage
                p_parameters["At cage edge [%]"] = cage_edge_time_percentage

            elif p_parameters_df_initialized:
                p_parameters.append(median_speed_val)
                p_parameters.append(distance_per_min)
                p_parameters.append(immobile_percentage)
                p_parameters.append(cage_edge_time_percentage)


        #metadata = get_metadata(file)
        """
        if not p_parameters_df_initialized:
            p_parameters = {
                            "Stimulus to total investigation DLC [%]": perc_total_inv_dlc,
                            "Total investigation time DLC [%]": total_inv_dlc,
                            "Discrimination Index DLC": disc_ind_dlc,
                            "Stimulus investigation events DLC": dlc_stim_event_count,
                            "Stimulus to total investigation DEG [%]": perc_total_inv_deg,
                            "Total investigation time DEG [%]": total_inv_deg,
                            "Discrimination Index DEG": disc_ind_deg,
                            "Median speed [km/h]": median_speed_val,
                            "Distance per minute [m]": distance_per_min,
                            "Immobile time [%]": immobile_percentage
                            }
            p_parameters_df = ini_processed_parameters_df(processed_parameters=p_parameters, metadata_dic=metadata)
            p_parameters_df_initialized = True

        elif p_parameters_df_initialized:
            p_parameters = [
                            perc_total_inv_dlc, 
                            total_inv_dlc,
                            disc_ind_dlc,
                            dlc_stim_event_count,
                            perc_total_inv_deg,
                            total_inv_deg,
                            disc_ind_deg,
                            median_speed_val,
                            distance_per_min,
                            immobile_percentage
                            ]
            p_parameters_df = append_processed_parameters_df(processed_parameters_df=p_parameters_df,processed_parameters=p_parameters,metadata_dic=metadata)
        """
        if not p_parameters_df_initialized:
            p_parameters_df = ini_processed_parameters_df(processed_parameters=p_parameters, metadata_dic=metadata)
            p_parameters_df_initialized = True
        elif p_parameters_df_initialized:
            p_parameters_df = append_processed_parameters_df(processed_parameters_df=p_parameters_df,processed_parameters=p_parameters,metadata_dic=metadata)
        # parameter file goes to the respective 'done' folder
        if move_para_file:
            shutil.move(file, path_parameters_done)


    save_hab_exp(p_parameters_df, output_path=f"{project_path}/processed/processed_parameters/")

# # # # End: Take processed (parameter) data, calculate metrics, save metrics of similar paradigm recordings in one csv  # # # #


    
   