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
    speed = calculate_speed(distance)
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
    parameters = {"distance_travelled_center":distance,
                "speed_in_km/h":speed,
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

    
    # AB HIER TESTCODE FÜR FIGURES

    print(sum(is_investigating_left))
    print(sum(is_investigating_right)/len(is_investigating_right))
    plt.figure(figsize=(10,6))
    data_left = np.where(is_investigating_left == 1)[0]
    data_right = np.where(is_investigating_right == 1)[0]
    data_left_norm = (data_left / len(is_investigating_left))
    data_right_norm = (data_right / len(is_investigating_right))
    plt.eventplot(data_left_norm, lineoffsets="left", colors="b") 
    plt.eventplot(data_right_norm, lineoffsets="right", colors="r")
    plt.xlim(0, 1)
    plt.legend()
    plt.xlabel('Video duration')
    plt.title(f"Mouse: {metadata['mouse']}; Paradigm: {metadata['paradigm']}; Date: {metadata['date']}")
    plt.savefig(f"./testing/{metadata['date']}_{metadata['mouse']}_{metadata['paradigm']}.svg", format='svg')
    plt.show()
   