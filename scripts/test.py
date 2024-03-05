
import glob
from tqdm import tqdm
import time

from get_metadata import get_metadata
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from save_to_csv import metadata_bodyparts_to_csv, parameters_to_csv
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object, distance_bodypart_bodypart,time_spent_sides,investigation_time,immobile_time

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



path = "C:/Users/quicken/Code/SimonAnalysisPipeline/raw/*"
file_list = glob.glob(path)



for file in tqdm(file_list):
    time.sleep(0.5)

    df = rewrite_dataframe(csv_file_path=file)
    metadata = get_metadata(csv_file_path=file)
    new_df = get_bodypart(df_all_bp=df,bodypart_list=["nose", "left_dish", "right_dish", "center", "topleft", "topright"])
    print("\nGet distance values...")
    distance = distance_travelled(data = new_df, bodypart = "center")
    print("\nGet speed values...")
    speed = calculate_speed(distance)
    print("\nGet immobile time...")
    is_immobile = immobile_time(speed_values=speed)
    print("\nGet distance to left dish...")
    distance_to_leftdish = distance_bodypart_object(data=new_df,bodypart="nose",object="left_dish")
    print("\nGet distance to right dish...")
    distance_to_rightdish = distance_bodypart_object(data=new_df,bodypart="nose",object="right_dish")
    print("\nGet time spent on either cagehalf...")
    is_left, is_right = time_spent_sides(data = new_df,bodypart="center",edge_left="topleft", edge_right="topright")
    print("\nGet dish investigation left...")
    is_investigating_left = investigation_time(distance_to_leftdish,factor=1.5)
    print("\nGet dish investigation right...")
    is_investigating_right = investigation_time(distance_to_rightdish,factor=1.5)


    parameters = {"distance_travelled_center":distance,
                "speed_in_hm/h":speed,
                "is_immobile":is_immobile,
                "distance_nose_leftdish":distance_to_leftdish,
                "distance_nose_rightdish":distance_to_rightdish,
                "is_left_cagehalf": is_left,
                "is_right_cagehalf": is_right,
                "is_investigating_leftdish": is_investigating_left,
                "is_investigating_rightdish": is_investigating_right}


    metadata_bodyparts_to_csv(metadata_dic=metadata,bodyparts_df=new_df,path="./processed/")
    parameters_to_csv(metadata_dic=metadata,parameters=parameters,path="./processed/")

    










   
    



