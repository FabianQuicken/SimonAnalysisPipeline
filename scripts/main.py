
import glob
from tqdm import tqdm
import time
import pandas as pd
import numpy as np
import shutil

from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv, ini_processed_parameters_df, append_processed_parameters_df, processed_bodyparts_to_csv, append_to_existing_csv
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object, distance_bodypart_bodypart,time_spent_sides,investigation_time,immobile_time
from further_processing import percent_of_total_inv_time, disc_index, total_inv_time, median_speed, full_distance, full_immobile_time

"""
!!! HOW TO USE THE CODE !!!

You need DeepLabCut .csv files.
The files will get loaded first.
get_df() creates a df from a path.

The configurations.py contains 

Then a new DataFrame needs to be generated to get 
rid of the weird DLC table. (rewrite_dataframe())
The new dataframe contains columns of all predicitons, with 
column headings in the style of: prediction_1_x,
                                 prediction_1_y, 
                                 prediction_1_likelihood,
                                 prediction_2_x,
                                 ...,

Next, a new DataFrame can get generated containing 
only predictions of interest passed to get_bodypart()
with a list of strings.
This df can be expanded as needed.



"""


# get path of all files
path = "./raw/new/*"
path_done = "./raw/done/"
file_list = glob.glob(path)

# calculate basic parametersfrom dlc data
for file in tqdm(file_list):
    time.sleep(0.5)

    df = rewrite_dataframe(csv_file_path=file) # rewrites the dataframe of dlc for easier readibility
    metadata = get_metadata(csv_file_path=file) # get metadata from the file name
    new_df = get_bodypart(df_all_bp=df,bodypart_list=["nose", "left_dish", "right_dish", "center", "topleft", "topright"]) # new df 
    # only containing bodypart data used for calculations
    print("\nGet distance values...")
    distance = distance_travelled(data = new_df, bodypart = "center")
    print("\nGet speed values...")
    speed = calculate_speed(distance)
    print("\nGet immobile time...")
    is_immobile, immobile_threshold = immobile_time(speed_values=speed)
    print("\nGet distance to left dish...")
    distance_to_leftdish = distance_bodypart_object(data=new_df,bodypart="nose",object="left_dish")
    print("\nGet distance to right dish...")
    distance_to_rightdish = distance_bodypart_object(data=new_df,bodypart="nose",object="right_dish")
    print("\nGet time spent on either cagehalf...")
    is_left, is_right = time_spent_sides(data = new_df,bodypart="center",edge_left="topleft", edge_right="topright")
    print("\nGet dish investigation left...")
    is_investigating_left, factor = investigation_time(distance_to_leftdish,factor=1.5)
    print("\nGet dish investigation right...")
    is_investigating_right, factor = investigation_time(distance_to_rightdish,factor=1.5)

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

    # bodyparts for calculations & parameters get saved to new csv's, respectively
    metadata_bodyparts_to_csv(metadata_dic=metadata,bodyparts_df=new_df,path="./processed/bodyparts/")
    parameters_to_csv(metadata_dic=metadata,parameters=parameters,path="./processed/parameters/new/")

    shutil.move(file, path_done)


# further postprocessing steps, based on the parameters
path_parameters = "./processed/parameters/new/*"
path_parameters_done = "./processed/parameters/done/"
file_list_parameters = glob.glob(path_parameters)
p_parameters_df_initialized = False


for file in tqdm(file_list_parameters):
    time.sleep(0.5)

    metadata = get_metadata(csv_file_path=file)
    print(metadata)
    parameters_df = pd.read_csv(file)

    perc_total_inv, exp_or_hab = percent_of_total_inv_time(metadata,parameters_df)
    total_inv = total_inv_time(metadata, parameters_df)
    disc_ind = disc_index(metadata, parameters_df)
    median_speed_val = median_speed(parameters_df)
    distance_per_min = full_distance(parameters_df)
    immobile_percentage = full_immobile_time(parameters_df)

    metadata = get_metadata(file)

    if not p_parameters_df_initialized:
        p_parameters = {"Stimulus to total investigation [%]": perc_total_inv,
                        "Total investigation time [%]": total_inv,
                        "Discrimination Index": disc_ind,
                        "Median speed [km/h]": median_speed_val,
                        "Distance per recording [m]": distance_per_min,
                        "Immobile time [%]": immobile_percentage}
        p_parameters_df = ini_processed_parameters_df(processed_parameters=p_parameters, metadata_dic=metadata)
        p_parameters_df_initialized = True

    elif p_parameters_df_initialized:
        p_parameters = [perc_total_inv,total_inv,disc_ind,median_speed_val,distance_per_min,immobile_percentage]
        p_parameters_df = append_processed_parameters_df(processed_parameters_df=p_parameters_df,processed_parameters=p_parameters,metadata_dic=metadata)
    
    shutil.move(file, path_parameters_done)


df_habituation = p_parameters_df[p_parameters_df.index.str.contains('Habituation')]
df_experiment = p_parameters_df[p_parameters_df.index.str.contains('Experiment')]




try:
    append_to_existing_csv(existing_csv_path="./processed/processed_parameters/experiment_processed_parameters.csv", new_df=df_experiment)
except:
    processed_bodyparts_to_csv(habituation=False, p_parameters=df_experiment, path="./processed/processed_parameters/")

try:
    append_to_existing_csv(existing_csv_path="./processed/processed_parameters/habituation_processed_parameters.csv", new_df=df_habituation)
except:
    processed_bodyparts_to_csv(habituation=True, p_parameters=df_habituation, path="./processed/processed_parameters/")


 











   
    



