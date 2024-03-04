
import glob
from configurations import mice, paradigms, networks, cameras
import pandas as pd
import numpy as np

from get_metadata import get_metadata
from save_metadata_in_df import save_metadata_in_df
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from likelihood_filter import likelihood_filtering,likelihood_filtering_nans
from save_to_csv import metadata_bodyparts_to_csv
from calculate_parameters import distance_travelled, calculate_speed, distance_bodypart_object, distance_bodypart_bodypart,time_spent_sides

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
only predictions of interest via get_bodypart().
This df can be expanded as needed.

"""



path = "C:/Users/quicken/Code/SimonAnalysisPipeline/raw/*"
file_list = glob.glob(path)
print(file_list)

"""
for file in file_list:
    print(save_metadata_in_df(get_metadata(file)))
"""

df = rewrite_dataframe(csv_file_path=file_list[0])

metadata = get_metadata(csv_file_path=file_list[0])

metadata = save_metadata_in_df(metadata)
#metadata = metadata.T

#metadata = metadata.rename(columns={0:"Metadata"})


new_df = get_bodypart(df_all_bp=df, bodypart="nose")
#new_df = likelihood_filtering_nans(df=new_df, likelihood_row_name="nose_likelihood", filter_val=0.95)
new_df = get_bodypart(df_all_bp=df, df_spec_bp=new_df, bodypart="left_dish")
new_df = get_bodypart(df_all_bp=df, df_spec_bp=new_df, bodypart="right_dish")
new_df = get_bodypart(df_all_bp=df, df_spec_bp=new_df, bodypart="center")
new_df = get_bodypart(df_all_bp=df, df_spec_bp=new_df, bodypart="topleft")
new_df = get_bodypart(df_all_bp=df, df_spec_bp=new_df, bodypart="topright")
distance = distance_travelled(data = new_df, bodypart = "center")
speed = calculate_speed(distance)
distance_to_leftdish = distance_bodypart_object(data=new_df,bodypart="nose",object="left_dish")
distance_to_rightdish = distance_bodypart_object(data=new_df,bodypart="nose",object="right_dish")
is_left, is_right = time_spent_sides(data = new_df,bodypart="center",edge_left="topleft", edge_right="topright")






#metadata_bodyparts_to_csv(bodyparts_df=new_df,metadata_df=metadata, path="C:/Code/SimonAnalysisPipeline/processed/new_save.csv")





   
    



