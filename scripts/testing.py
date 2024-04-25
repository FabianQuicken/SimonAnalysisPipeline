import glob
from tqdm import tqdm
import time
import pandas as pd
import numpy as np
import shutil
import matplotlib.pyplot as plt

from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv, ini_processed_parameters_df, append_processed_parameters_df, save_hab_exp
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object,time_spent_sides,investigation_time,immobile_time
from further_processing import percent_of_total_inv_time, disc_index, total_inv_time, median_speed, full_distance, full_immobile_time
from get_parameters import find_parameter_file
from figures import eventplot, pieplot, plot_cum_dist, plot_distance_val

path = "./testing/raw/*"
path_done = "./testing/done/"
file_list = glob.glob(path)


# calculate basic parametersfrom dlc data
for file in tqdm(file_list):
    time.sleep(0.5)

    df = rewrite_dataframe(csv_file_path=file) # rewrites the dataframe of dlc for easier readibility
    metadata = get_metadata(csv_file_path=file) # get metadata from the file name
    # new df only containing bodypart data used for calculations
    new_df = get_bodypart(df_all_bp=df,bodypart_list=["nose", "left_dish", "right_dish", "center", "topleft", "topright"])  
    
    # getting all the parameters from the DLC Data
    distance = distance_travelled(df = new_df, bodypart = "center")

   
    speed = calculate_speed(distance_array=distance)
    is_immobile, immobile_threshold = immobile_time(speed_values=speed)
    distance_to_leftdish = distance_bodypart_object(df=new_df,bodypart="nose",object="left_dish")
    distance_to_rightdish = distance_bodypart_object(df=new_df,bodypart="nose",object="right_dish")
    is_left, is_right = time_spent_sides(df = new_df,bodypart="center",edge_left="topleft", edge_right="topright")
    print("\nGet dish investigation left...")
    is_investigating_left, factor = investigation_time(distance_to_leftdish,factor=2.2)
    print("\nGet dish investigation right...")
    is_investigating_right, factor = investigation_time(distance_to_rightdish,factor=2.2)
    # adding array containing information about the radius used for petridish investigation 
    radius_petridish = np.zeros(len(is_investigating_left))
    for i in range(len(radius_petridish)-1):
        radius_petridish[i] = factor
    # adding array containing information about the speed threshold for immobile behavior
    immobile_speeds = np.zeros(len(is_immobile))
    for i in range(len(immobile_speeds)-1):
        immobile_speeds[i] = immobile_threshold
    # write parameters into a dic; new calculations need to be appended manually
    parameters = {"distance_travelled_center[cm]":distance,
                "speed[km/h]":speed,
                "is_immobile":is_immobile,
                "immobile_threshold[km/h]": immobile_speeds,
                "distance_nose_leftdish":distance_to_leftdish,
                "distance_nose_rightdish":distance_to_rightdish,
                "center_is_left_cagehalf": is_left,
                "center_is_right_cagehalf": is_right,
                "is_investigating_leftdish": is_investigating_left,
                "is_investigating_rightdish": is_investigating_right,
                "petridish_investigation_radius[cm]": radius_petridish
                }
    print(np.nanmean(speed))
    
    # AB HIER TESTCODE FÜR FIGURES
    
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

# # # # Start: Get data from DeepEthogram, append it to the respective parameters files # # # #

# define the paths and get the deg files
deg_path = "./testing/deg_raw/*"
deg_path_done = "./raw/deg_done/"
deg_file_list = glob.glob(deg_path)

# get all possible parameter paths
parameter_new_path = "./processed/parameters/new/*"
parameter_new_list = glob.glob(parameter_new_path)
parameter_done_path = "./processed/parameters/done/*"
parameter_done_list = glob.glob(parameter_done_path)
parameter_full_list = parameter_new_list + parameter_done_list

for deg_file in tqdm(deg_file_list):
    time.sleep(0.5)

    # get the DeepEthogram dataframe and the matching parameter_df
    deg_metadata = get_metadata(deg_file)
    deg_df = pd.read_csv(deg_file)
    parameter_df, parameter_df_path = find_parameter_file(deg_file=deg_file, metadata_dic=deg_metadata, parameter_paths=parameter_full_list)

    # append DeepEthogram data to the parameter_df
    parameter_df["deg_is_investigating_leftdish"] = np.array(deg_df["leftsniffing"])
    parameter_df["deg_is_investigating_rightdish"] = np.array(deg_df["rightsniffing"])

    eventplot(metadata=deg_metadata,
              save_name="investigation_behavior", 
              data_list=[deg_df["leftsniffing"], deg_df["rightsniffing"]], 
              lineoffsets=["deg sniff left dish", "def sniff right dish"],
              colors=["m","y"],
              skip_frame_stepsize=4)


    
    
# # # # End: Get data from DeepEthogram, append it to the respective parameters files # # # #

    
    

    
   