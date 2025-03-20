import pandas as pd
import glob
from mathematics import euklidean_distance
import numpy as np

def likelihood_filtering(df, likelihood_row_name=str, filter_val = 0.95):
    """
    DeepLabCut provides a likelihood for the prediction of 
    each bodypart in each frame to be correct. Filtering predictions
    for the likelihood, reduces false predictions in the dataset.
    """
    df_filtered = df.copy()
    df_filtered = df[df[likelihood_row_name] > filter_val]
    df_removed_rows = df[df[likelihood_row_name] < filter_val]
    #print(f"The filter removed {len(df_removed_rows)} rows of a total of {len(df)} rows.")
    return df_filtered

def likelihood_filtering_nans(df, likelihood_row_name=str, filter_val=0.60):
    """
    DeepLabCut provides a likelihood for the prediction of 
    each bodypart in each frame to be correct. Filtering predictions
    for the likelihood, replaces values in the entire row with NaN where the likelihood is below the filter_val.
    """
    df_filtered = df.copy()  # Make a copy to avoid modifying the original DataFrame
    filtered_rows = df_filtered[likelihood_row_name] < filter_val
    df_filtered.loc[filtered_rows] = np.nan
    num_replaced = filtered_rows.sum()
    #print(f"The filter replaced values in {num_replaced} rows with NaN out of a total of {len(df)} rows.")
    return df_filtered

def distance_bodypart_object(df, bodypart=str, object=str):
    """
    Takes a Dataframe, a bodypart and an object as strings,
    to calculate the distance between both.
    Note: Df gets likelihood filtered for bodypart first.
    Object should not move during recording, since
    the first good prediction will be set to the object location.
    """
    data = df.copy()
    """
    print(f"\nGet distance {bodypart} to {object}...")
    print(f"Filtering {bodypart} for object distance calculation...")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart+"_likelihood")
    """
    bodypart_x = data[bodypart+"_x"]
    bodypart_y = data[bodypart+"_y"]
    

    #print("Filtering for a good object prediction...")
    data = likelihood_filtering(df=data, 
                                likelihood_row_name=object+"_likelihood",
                                filter_val=0.95)
    object_x = data[object+"_x"]
    object_y = data[object+"_y"]


    bodypart_x = np.array(bodypart_x)
    bodypart_y = np.array(bodypart_y)
    object_x = np.array(object_x)
    object_y = np.array(object_y)
    object_x = object_x[0]
    object_y = object_y[0]


    distance_values = np.zeros((len(bodypart_x)))
    for i in range(len(bodypart_x)-1):
        distance_values[i] = euklidean_distance(x1=bodypart_x[i],
                                                y1=bodypart_y[i],
                                                x2=object_x,
                                                y2=object_y)
    return distance_values


"""
for file in csv_files:
    df = pd.read_csv(file,names=df_cols)
    data = df.copy()
    data = data.iloc[4:]
    data = data.astype(float)

    df_spec_bp = pd.DataFrame()
    df_bp = df_spec_bp.copy()
    for bodypart in bodyparts:
        df_bp[bodypart+"_x"] = data[bodypart+"_x"]
        df_bp[bodypart+"_y"] = data[bodypart+"_y"]
        df_bp[bodypart+"_likelihood"] = data[bodypart+"_likelihood"]
    df_bp.to_csv(file + "rewritten.csv")
"""

pixel_per_cm=34.77406

project_path = "./isot/Odor Investigation/Evaluation"
dlc_raw_path = f"{project_path}/dist_thresh/*.csv"
csv_files = glob.glob(dlc_raw_path)
"""
distance_thresh = 0
for i in range(150):
    
    for file in csv_files:
        df = pd.read_csv(file)
        data = df.copy()

        snout_likelihood =  data["nose_likelihood"]
        dist_snout_leftdish = distance_bodypart_object(df=data, bodypart="nose", object="left_dish")
        dist_snout_rightdish = distance_bodypart_object(df=data, bodypart="nose", object="right_dish")

        

        left_invest = np.zeros(len(dist_snout_leftdish))
        right_invest = np.zeros(len(dist_snout_rightdish))

        nan_values = np.zeros(len(snout_likelihood))

        for i in range(len(dist_snout_leftdish)):
            if dist_snout_leftdish[i] <= distance_thresh:
                left_invest[i] = 1

            if dist_snout_rightdish[i] <= distance_thresh:
                right_invest[i] = 1            


            # count NaN true positives in ground truth
            if snout_likelihood[i] < 0.6:
                nan_values[i] = 1


        odor_inv = {"left investigation": left_invest,
                        "right investigation": right_invest,
                        "nose nan": nan_values}
        

        output_df = pd.DataFrame(odor_inv)

        output_df.to_csv(file + f"odor_inv_{distance_thresh}.csv")

        distance_thresh +=1
"""

# optimale dist_threshs: 60

distance_thresh = 60

for file in csv_files:
    df = pd.read_csv(file)
    data = df.copy()

    snout_likelihood =  data["nose_likelihood"]
    dist_snout_leftdish = distance_bodypart_object(df=data, bodypart="nose", object="left_dish")
    dist_snout_rightdish = distance_bodypart_object(df=data, bodypart="nose", object="right_dish")

    left_invest = np.zeros(len(dist_snout_leftdish))
    right_invest = np.zeros(len(dist_snout_rightdish))


    nan_values = np.zeros(len(snout_likelihood))

    for i in range(len(dist_snout_leftdish)):
        if dist_snout_leftdish[i] <= distance_thresh:
            left_invest[i] = 1

        if dist_snout_rightdish[i] <= distance_thresh:
            right_invest[i] = 1    


    odor_inv = {"left investigation": left_invest,
                    "right investigation": right_invest,
                    "nose nan": nan_values}
        

    output_df = pd.DataFrame(odor_inv)

    output_df.to_csv(file + f"odor_inv_{distance_thresh}.csv")
