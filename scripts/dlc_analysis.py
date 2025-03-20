import glob
from tqdm import tqdm
import time
import numpy as np
import shutil
import os


from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object,time_spent_sides,investigation_time,immobile_time






def dlc_analysis(project_path=str,
                 dlc_layout=tuple,
                 used_bodyparts=list, 
                 calc_distance_and_speed=bool, 
                 distance_bodypart=str, 
                 calc_immobile_time=bool, 
                 immobile_threshold=float,
                 calc_dist_left_object=bool,
                 obj_dist_bodypart=str,
                 left_obj=str,
                 calc_dist_right_object=bool,
                 right_obj=str,
                 calc_side_pref=bool,
                 side_pref_bodypart=str,
                 left_edge=str,
                 right_edge=str,
                 calc_inv_time=bool,
                 save_bodyparts=bool,
                 save_parameters=bool,
                 move_raw_csv=bool
                 ):

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