import glob
from tqdm import tqdm
import time
import pandas as pd
import numpy as np
import shutil
import os

from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv, ini_processed_parameters_df, append_processed_parameters_df, save_hab_exp
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object,time_spent_sides,investigation_time,immobile_time
from further_processing import percent_of_total_inv_time, disc_index, total_inv_time, median_speed, full_distance, full_immobile_time
from get_parameters import find_parameter_file
from configurations import dlc_petridish_layout_fabi, dlc_petridish_layout_simon, dlc_mighty_snicket_layout_simon
from split_exp_hab import split_csv, split_csv_chatgpt
from figures import eventplot, pieplot, plot_cum_dist, plot_distance_val

#from move_file import move_file

# # # # !!! EDIT THE CODE ONLY HERE !!! # # # # 
# # # # Define your experiment here # # # #

# define the project path - head directory of your specific dataset, that should be analyzed similarly
project_path = "./datasets/FQ_petridishes_female_urine"
# what objects were labelled?
left_obj = "leftpetridish"
right_obj = "rightpetridish"

# do you want to process dlc csv files?
dlc_analysis = False
if dlc_analysis:
    # the dlc layout contains information about the column names of the bodyparts
    dlc_layout = dlc_petridish_layout_fabi

    # define the bodyparts you want to extract out of the df for further calculations
    used_bodyparts = ["snout", "leftpetridish", "rightpetridish", "centroid", "topleft", "topright"]


    calc_distance_and_speed = True
    # what bodypart do you want to use for distance and speed calculation?
    distance_bodypart = "centroid"

    calc_immobile_time = True
    # below what speed threshold [km/h] the animal is defined immobile?
    immobile_threshold = 0.05

    calc_dist_left_object = True
    calc_dist_right_object = True
    # what bodypart is used for distance calculation?
    obj_dist_bodypart = "snout"

    # do you want to calculate investigation behavior based on the distance?
    calc_inv_time = True

    calc_side_pref = True
    # give the bodypart that is checked for sidepref
    side_pref_bodypart = "centroid"
    # give two coordinates that define the edges of the arena
    # will be used to 'draw' a center line 
    left_edge = "topleft"
    right_edge = "topright"

    # do you want to save the used bodyparts in an extra csv?
    save_bodyparts = True

    # do you want to save the calculated parameters to a csv?
    save_parameters = True

    # do you want to move the raw dlc csv's from 'new' to 'done' folder?
    move_raw_csv = True

# do you want to add deg data to existing parameter files?
add_deg_data = True
if add_deg_data:
    # how are deg behaviors labelled?
    deg_behavior1 = '"SniffLeftDish'
    deg_behavior2 = 'SniffRightDish"'

    # how should the column be indexed in the parameter files?
    behavior1_index = "deg_is_investigating_left_dish"
    behavior2_index = "deg_is_investigating_right_dish"

    # do you want to move the deg_csvs to the 'done' directory?
    move_deg_csv = True

# do you want to do postprocessing?
run_postprocessing = False
if run_postprocessing:
    # should the parameter file be moved in the 'done' directory?
    move_para_file = True

make_plots = False

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
        metadata = get_metadata(csv_file_path=file) # get metadata from the file name
        # new df only containing bodypart data used for calculations
        new_df = get_bodypart(df_all_bp=df,bodypart_list=used_bodyparts)  


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
            is_investigating_left, factor = investigation_time(distance_to_left_object,factor=2)
            print("\nGet dish investigation right...")
            is_investigating_right, factor = investigation_time(distance_to_right_object,factor=2)
            # adding array containing information about the radius used for petridish investigation 
            radius_petridish = np.zeros(len(is_investigating_left))
            for i in range(len(radius_petridish)-1):
                radius_petridish[i] = factor
            parameters[f"is_investigating_{left_obj}"] = is_investigating_left
            parameters[f"is_investigating_{right_obj}"] = is_investigating_right
            parameters["object_investigation_radius[cm]"] = radius_petridish
        """
        # write parameters into a dic; new calculations need to be appended manually
        parameters = {"distance_travelled_center":distance,
                    "speed_in_km/h":speed,
                    "is_immobile":is_immobile,
                    "immobile_threshold[km/h]": immobile_speeds,
                    "distance_nose_left_snicket":distance_to_left_object,
                    "distance_nose_right_snicket":distance_to_right_object,
                    "center_is_left_cagehalf": is_left,
                    "center_is_right_cagehalf": is_right,
                    "is_investigating_leftdish": is_investigating_left,
                    "is_investigating_rightdish": is_investigating_right,
                    "petridish_investigation_radius[cm]": radius_petridish
                    }
        """

        # bodyparts for calculations & parameters get saved to new csv's, respectively
        if save_bodyparts:
            metadata_bodyparts_to_csv(metadata_dic=metadata,bodyparts_df=new_df,path=f"{project_path}/processed/bodyparts/")
        if save_parameters:
            parameters_to_csv(metadata_dic=metadata,parameters=parameters,path=f"{project_path}/processed/parameters/new/")

        # dlc file goes to the respective 'done' folder
        if move_raw_csv:
            shutil.move(file, path_done)

# # # # End: Get data from DeepLabCut, calculate parameters, save used bodyparts and parameters as csv  # # # #

# # # # Start: Get data from DeepEthogram, append it to the respective parameters files # # # #

# define the paths and get the deg files
if add_deg_data:
    deg_path = f"{project_path}/raw/deg_new/*.csv"
    deg_path_done = f"{project_path}/raw/deg_done/"
    deg_file_list = glob.glob(deg_path)



    # get all possible parameter paths
    parameter_new_path = f"{project_path}/processed/parameters/new/*.csv"
    parameter_new_list = glob.glob(parameter_new_path)

    parameter_done_path = f"{project_path}/processed/parameters/done/*.csv"
    parameter_done_list = glob.glob(parameter_done_path)
    parameter_full_list = parameter_new_list + parameter_done_list

    for deg_file in tqdm(deg_file_list):
        time.sleep(0.2)

        # get the DeepEthogram dataframe and the matching parameter_df
        deg_metadata = get_metadata(deg_file)
        deg_df = pd.read_csv(deg_file)

        parameter_df, parameter_df_path = find_parameter_file(deg_file=deg_file, metadata_dic=deg_metadata, parameter_paths=parameter_full_list)

        # append DeepEthogram data to the parameter_df
        try:
            parameter_df[behavior1_index] = np.array(deg_df[deg_behavior1])
            parameter_df[behavior2_index] = np.array(deg_df[deg_behavior2])
        except:
            print("WARNING: DEG behavior lenght did not match the DLC data !!!!")
            parameter_df = parameter_df.reindex(range(len(deg_df[deg_behavior2])))
            parameter_df[behavior1_index] = np.array(deg_df[deg_behavior1])
            parameter_df[behavior2_index] = np.array(deg_df[deg_behavior2])

        # save the new parameter_df to the same file
        parameter_df.to_csv(parameter_df_path)

        if move_deg_csv:
            # used deg file goes to the respective 'done' folder
            shutil.move(deg_file, deg_path_done)
    
# # # # End: Get data from DeepEthogram, append it to the respective parameters files # # # #

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

    for file in tqdm(file_list_parameters):
        print(f"Working on file: {file}")
        time.sleep(0.2)

        metadata = get_metadata(csv_file_path=file)
        parameters_df = pd.read_csv(file)

        perc_total_inv_dlc, perc_total_inv_deg, exp_or_hab = percent_of_total_inv_time(metadata,parameters_df, left_obj=left_obj, right_obj=right_obj)
        total_inv_dlc, total_inv_deg = total_inv_time(metadata, parameters_df, left_obj=left_obj, right_obj=right_obj)
        disc_ind_dlc, disc_ind_deg = disc_index(metadata, parameters_df, left_obj=left_obj, right_obj=right_obj)
        median_speed_val = median_speed(parameters_df)
        distance_per_min = full_distance(parameters_df)
        immobile_percentage = full_immobile_time(parameters_df)

        metadata = get_metadata(file)

        if not p_parameters_df_initialized:
            p_parameters = {"Stimulus to total investigation DLC [%]": perc_total_inv_dlc,
                            "Total investigation time DLC [%]": total_inv_dlc,
                            "Discrimination Index DLC": disc_ind_dlc,
                            "Stimulus to total investigation DEG [%]": perc_total_inv_deg,
                            "Total investigation time DEG [%]": total_inv_deg,
                            "Discrimination Index DEG": disc_ind_deg,
                            "Median speed [km/h]": median_speed_val,
                            "Distance per minute [m]": distance_per_min,
                            "Immobile time [%]": immobile_percentage}
            p_parameters_df = ini_processed_parameters_df(processed_parameters=p_parameters, metadata_dic=metadata)
            p_parameters_df_initialized = True

        elif p_parameters_df_initialized:
            p_parameters = [perc_total_inv_dlc, total_inv_dlc, disc_ind_dlc, perc_total_inv_deg, total_inv_deg, disc_ind_deg, median_speed_val, distance_per_min, immobile_percentage]
            p_parameters_df = append_processed_parameters_df(processed_parameters_df=p_parameters_df,processed_parameters=p_parameters,metadata_dic=metadata)

        # parameter file goes to the respective 'done' folder
        if move_para_file:
            shutil.move(file, path_parameters_done)


    save_hab_exp(p_parameters_df, output_path=f"{project_path}/processed/processed_parameters/")

# # # # End: Take processed (parameter) data, calculate metrics, save metrics of similar paradigm recordings in one csv  # # # #

if make_plots:

    path_parameters = f"{project_path}/processed/parameters/done/*.csv"
    path_save_figs = f"{project_path}/figures/"
    file_list_parameters = glob.glob(path_parameters)

    for file in tqdm(file_list_parameters):
        print(f"Working on file: {file}")
        time.sleep(0.2)

        metadata = get_metadata(csv_file_path=file)
        parameters_df = pd.read_csv(file)


        
        eventplot(metadata=metadata,
                save_name=f"investigation_behavior_{factor}cm_radius", 
                data_list=[is_investigating_left, is_investigating_right], 
                lineoffsets=["dlc left dish", "dlc right dish"],
                colors=["m","y"],
                skip_frame_stepsize=4)
        

        pieplot(metadata=metadata,data_list=[is_left,is_right], save_name="side_preference",colors=["m","y"],labels=["is left", "is right"])

        eventplot(metadata=metadata,
                save_name="immobile_behavior",
                data_list=[is_immobile],
                lineoffsets=["is_immobile"],
                colors=['b'],
                skip_frame_stepsize=20)


        plot_cum_dist(metadata=metadata,arr=distance, save_name="dist_travelled", color='m')

        plot_distance_val(metadata=metadata, data_list=[distance_to_leftdish, distance_to_rightdish], colors=['m', 'y'],save_name='dish_distances',labels=['leftdish', 'rightdish'])

        eventplot(metadata=deg_metadata,
                save_name="investigation_behavior", 
                data_list=[deg_df["leftsniffing"], deg_df["rightsniffing"]], 
                lineoffsets=["deg sniff left dish", "def sniff right dish"],
                colors=["m","y"],
                skip_frame_stepsize=4)