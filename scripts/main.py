
import glob
from tqdm import tqdm
import time
import pandas as pd
import numpy as np
import shutil

from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv, ini_processed_parameters_df, append_processed_parameters_df, save_hab_exp
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object,time_spent_sides,investigation_time,immobile_time
from further_processing import percent_of_total_inv_time, disc_index, total_inv_time, median_speed, full_distance, full_immobile_time
from get_parameters import find_parameter_file
from configurations import dlc_petridish_layout_fabi

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


# # # # Start: Get data from DeepLabCut, calculate parameters, save used bodyparts and parameters as csv  # # # #

# get path of all files
path = "./raw/dlc_new/*"
path_done = "./raw/dlc_done/"
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
    is_investigating_left, factor = investigation_time(distance_to_leftdish,factor=2)
    print("\nGet dish investigation right...")
    is_investigating_right, factor = investigation_time(distance_to_rightdish,factor=2)

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

    # dlc file goes to the respective 'done' folder
    shutil.move(file, path_done)

# # # # End: Get data from DeepLabCut, calculate parameters, save used bodyparts and parameters as csv  # # # #


    
# # # # Start: Get data from DeepEthogram, append it to the respective parameters files # # # #

# define the paths and get the deg files
deg_path = "./raw/deg_new/*"
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

    # save the new parameter_df to the same file
    parameter_df.to_csv(parameter_df_path)

    # used deg file goes to the respective 'done' folder
    shutil.move(deg_file, deg_path_done)
    
# # # # End: Get data from DeepEthogram, append it to the respective parameters files # # # #


    

# # # # Start: Take processed (parameter) data, calculate metrics, save metrics of similar paradigm recordings in one csv  # # # #

# set paths and get parameter data
path_parameters = "./processed/parameters/new/*"
path_parameters_done = "./processed/parameters/done/"
file_list_parameters = glob.glob(path_parameters)

# since we loop over multiple files and save everything into one file, we need one dataframe where all data is stored
# therefore, we first need to initialize the df, then append to it
# this variable checks, if a df was initialized and is first set to False
p_parameters_df_initialized = False

for file in tqdm(file_list_parameters):
    time.sleep(0.5)

    metadata = get_metadata(csv_file_path=file)
    parameters_df = pd.read_csv(file)

    perc_total_inv_dlc, perc_total_inv_deg, exp_or_hab = percent_of_total_inv_time(metadata,parameters_df)
    total_inv_dlc, total_inv_deg = total_inv_time(metadata, parameters_df)
    disc_ind_dlc, disc_ind_deg = disc_index(metadata, parameters_df)
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
                        "Distance per recording [m]": distance_per_min,
                        "Immobile time [%]": immobile_percentage}
        p_parameters_df = ini_processed_parameters_df(processed_parameters=p_parameters, metadata_dic=metadata)
        p_parameters_df_initialized = True

    elif p_parameters_df_initialized:
        p_parameters = [perc_total_inv_dlc, total_inv_dlc, disc_ind_dlc, perc_total_inv_deg, total_inv_deg, disc_ind_deg, median_speed_val, distance_per_min, immobile_percentage]
        p_parameters_df = append_processed_parameters_df(processed_parameters_df=p_parameters_df,processed_parameters=p_parameters,metadata_dic=metadata)
    
    # parameter file goes to the respective 'done' folder
    shutil.move(file, path_parameters_done)


save_hab_exp(p_parameters_df)

# # # # End: Take processed (parameter) data, calculate metrics, save metrics of similar paradigm recordings in one csv  # # # #


"""

 # # # # Start: Re-analysis of my own data # # # # 

path = "./raw/fabi/new/*"
path_done = "./raw/fabi/done/"
file_list = glob.glob(path)


for file in tqdm(file_list):
    time.sleep(0.5)

    df = rewrite_dataframe(csv_file_path=file,df_cols=dlc_petridish_layout_fabi) # rewrites the dataframe of dlc for easier readibility
    metadata = get_metadata(csv_file_path=file) # get metadata from the file name
    # new df only containing bodypart data used for calculations
    new_df = get_bodypart(df_all_bp=df,bodypart_list=["snout", "leftpetridish", "rightpetridish", "centroid", "topleft", "topright"]) 


    distance_to_leftdish = distance_bodypart_object(df=new_df,bodypart="snout",object="leftpetridish")
    distance_to_rightdish = distance_bodypart_object(df=new_df,bodypart="snout",object="rightpetridish")
    print("\nGet dish investigation left...")
    is_investigating_left, factor = investigation_time(distance_to_leftdish,factor=2.2)
    print("\nGet dish investigation right...")
    is_investigating_right, factor = investigation_time(distance_to_rightdish,factor=2.2)

    # adding array containing information about the radius used for petridish investigation 
    radius_petridish = np.zeros(len(is_investigating_left))
    for i in range(len(radius_petridish)-1):
        radius_petridish[i] = factor

    parameters = {"distance_nose_leftdish":distance_to_leftdish,
                "distance_nose_rightdish":distance_to_rightdish,
                "is_investigating_leftdish": is_investigating_left,
                "is_investigating_rightdish": is_investigating_right,
                "petridish_investigation_radius[cm]": radius_petridish
                }


    # bodyparts for calculations & parameters get saved to new csv's, respectively
    metadata_bodyparts_to_csv(metadata_dic=metadata,bodyparts_df=new_df,path="./processed/fabi/bodyparts/")
    parameters_to_csv(metadata_dic=metadata,parameters=parameters,path="./processed/fabi/parameters/new/")

    # dlc file goes to the respective 'done' folder
    shutil.move(file, path_done)

# set paths and get parameter data
path_parameters = "./processed/fabi/parameters/new/*"
path_parameters_done = "./processed/fabi/parameters/done/"
file_list_parameters = glob.glob(path_parameters)
print(file_list_parameters)

# since we loop over multiple files and save everything into one file, we need one dataframe where all data is stored
# therefore, we first need to initialize the df, then append to it
# this variable checks, if a df was initialized and is first set to False
p_parameters_df_initialized = False

for file in tqdm(file_list_parameters):
    time.sleep(0.5)

    metadata = get_metadata(csv_file_path=file)
    
    parameters_df = pd.read_csv(file)

    perc_total_inv_dlc, perc_total_inv_deg, exp_or_hab = percent_of_total_inv_time(metadata,parameters_df,dlc=True,deg=False)
    total_inv_dlc, total_inv_deg = total_inv_time(metadata, parameters_df,dlc=True,deg=False)
    disc_ind_dlc, disc_ind_deg = disc_index(metadata, parameters_df,dlc=True,deg=False)



    metadata = get_metadata(file)

    if not p_parameters_df_initialized:
        p_parameters = {"Stimulus to total investigation DLC [%]": perc_total_inv_dlc,
                        "Total investigation time DLC [%]": total_inv_dlc,
                        "Discrimination Index DLC": disc_ind_dlc
                        }
        
        p_parameters_df = ini_processed_parameters_df(processed_parameters=p_parameters, metadata_dic=metadata)
        p_parameters_df_initialized = True

    elif p_parameters_df_initialized:
        p_parameters = [perc_total_inv_dlc, total_inv_dlc, disc_ind_dlc]
        p_parameters_df = append_processed_parameters_df(processed_parameters_df=p_parameters_df,processed_parameters=p_parameters,metadata_dic=metadata)

    # parameter file goes to the respective 'done' folder
    shutil.move(file, path_parameters_done)

save_hab_exp(p_parameters_df, output_path="./processed/fabi/processed_parameters/")

"""


   
    



