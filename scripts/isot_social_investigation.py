"""

Was muss ich machen?
1. csv's einlesen
2. dataframe umschreiben
3. distance arrays generieren für alle benötigten abstände
4. behaviors definieren und arrays mit 0 bzw 1 füllen wenn abstände gegeben sind


"""

import pandas as pd
import glob
from mathematics import euklidean_distance
import numpy as np
# summen:
# gt_face_face = 1855, 1632, 4218
# gt_face_body = 4007, 4478, 9722
# gt_face_ass = 2986, 8055, 5887

def likelihood_filtering_nans(df, likelihood_row_name=str, filter_val=0.20):
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

def distance_bodypart_bodypart(df, bodypart_1=str, bodypart_2=str):
    """
    Takes a Dataframe and two bodyparts (can be 2 animals) as strings,
    to calculate the distance between both points
    Note: Df gets likelihood filtered for points of interest first.
    """
    data = df.copy()
    """
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart_1+"_likelihood")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart_2+"_likelihood")
    """
    bodypart_1_x = data[bodypart_1+"_x"]
    bodypart_1_y = data[bodypart_1+"_y"]
    bodypart_2_x = data[bodypart_2+"_x"]
    bodypart_2_y = data[bodypart_2+"_y"]

    bodypart_1_x = np.array(bodypart_1_x)
    bodypart_1_y = np.array(bodypart_1_y)
    bodypart_2_x = np.array(bodypart_2_x)
    bodypart_2_y = np.array(bodypart_2_y)

    distance_values = np.zeros((len(bodypart_1_x)))
    for i in range(len(bodypart_1_x)-1):
        distance_values[i] = euklidean_distance(x1=bodypart_1_x[i],
                                                y1=bodypart_1_y[i],
                                                x2=bodypart_2_x[i],
                                                y2=bodypart_2_y[i])
        distance_values[i] = distance_values[i]
    return distance_values

pixel_per_cm=34.77406

project_path = "./isot/Social Investigation/Evaluation"
dlc_raw_path = f"{project_path}/dlc_raw/*.csv"
csv_files = glob.glob(dlc_raw_path)
print(csv_files)

# csv's einlesen
df_cols = ("f_leftear_x", "f_leftear_y", "f_leftear_likelihood",
                        "f_rightear_x", "f_rightear_y", "f_rightear_likelihood",
                        "f_snout_x", "f_snout_y", "f_snout_likelihood",
                        "f_centroid_x", "f_centroid_y", "f_centroid_likelihood",
                        "f_lateralleft_x", "f_lateralleft_y", "f_lateralleft_likelihood",
                        "f_lateralright_x", "f_lateralright_y", "f_lateralright_likelihood",
                        "f_tailbase_x", "f_tailbase_y", "f_tailbase_likelihood",
                        "f_tailend_x", "f_tailend_y", "f_tailend_likelihood",
                        "m_leftear_x", "m_leftear_y", "m_leftear_likelihood",
                        "m_rightear_x", "m_rightear_y", "m_rightear_likelihood",
                        "m_snout_x", "m_snout_y", "m_snout_likelihood",
                        "m_centroid_x", "m_centroid_y", "m_centroid_likelihood",
                        "m_lateralleft_x", "m_lateralleft_y", "m_lateralleft_likelihood",
                        "m_lateralright_x", "m_lateralright_y", "m_lateralright_likelihood",
                        "m_tailbase_x", "m_tailbase_y", "m_tailbase_likelihood",
                        "m_tailend_x", "m_tailend_y", "m_tailend_likelihood",
                        )
bodyparts = ["f_snout", "f_lateralleft", "f_lateralright", "f_tailbase", "m_snout", "m_lateralleft", "m_lateralright", "m_tailbase"]
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


"""
distance_thresh = 0
for i in range(150):
    
    for file in csv_files:
        df = pd.read_csv(file)
        data = df.copy()
        dist_snout_snout = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_snout")
        dist_snout_f_lateral_l_m = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_lateralleft")
        dist_snout_f_lateral_r_m = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_lateralright")
        dist_snout_m_lateral_l_f = distance_bodypart_bodypart(df = data, bodypart_1="m_snout", bodypart_2="f_lateralleft")
        dist_snout_m_lateral_r_f = distance_bodypart_bodypart(df = data, bodypart_1="m_snout", bodypart_2="f_lateralright")
        dist_snout_f_tailbase_m = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_tailbase")
        dist_snout_m_tailbase_f = distance_bodypart_bodypart(df = data, bodypart_1="m_snout", bodypart_2="f_tailbase")
        snout_f = data["f_snout_x"]
        snout_m =  data["m_snout_x"]

        face_invest = np.zeros(len(dist_snout_snout))
        body_invest = np.zeros(len(dist_snout_snout))
        ass_invest = np.zeros(len(dist_snout_snout))
        nan_values_f = np.zeros(len(dist_snout_snout))
        nan_values_m = np.zeros(len(dist_snout_snout))

        for i in range(len(dist_snout_snout)):
            if dist_snout_snout[i] <= distance_thresh:
                face_invest[i] = 1
            
            if dist_snout_f_lateral_l_m[i] <=distance_thresh or dist_snout_f_lateral_r_m[i] <= distance_thresh or dist_snout_m_lateral_l_f[i] <= distance_thresh or dist_snout_m_lateral_r_f[i] <= distance_thresh:
                body_invest[i] = 1
            
            if dist_snout_f_tailbase_m[i] <=distance_thresh or dist_snout_m_tailbase_f[i] <=distance_thresh:
                ass_invest[i] = 1

            # count NaN true positives in ground truth
            if np.isnan(snout_f[i]):
                nan_values_f[i] = 1
            if np.isnan(snout_m[i]):
                nan_values_f[i] = 1

        social_behavior = {"face investigation": face_invest,
                        "body investigation": body_invest,
                        "anogenital investigation": ass_invest,
                        "f_nose nan": nan_values_f,
                        "m_nose nan": nan_values_m}
        

        output_df = pd.DataFrame(social_behavior)

        output_df.to_csv(file + f"social_behavior_{distance_thresh}.csv")

        distance_thresh +=1
"""
# optimale dist_threshs:
# anogenital: 65 (interpolated), 70 (raw)
# body: 80 (both)
# face: 70 (interpolated), 75 (raw)

dist_face = 75
dist_body = 80
dist_anogenital = 70

for file in csv_files:
    df = pd.read_csv(file)
    data = df.copy()
    dist_snout_snout = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_snout")
    dist_snout_f_lateral_l_m = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_lateralleft")
    dist_snout_f_lateral_r_m = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_lateralright")
    dist_snout_m_lateral_l_f = distance_bodypart_bodypart(df = data, bodypart_1="m_snout", bodypart_2="f_lateralleft")
    dist_snout_m_lateral_r_f = distance_bodypart_bodypart(df = data, bodypart_1="m_snout", bodypart_2="f_lateralright")
    dist_snout_f_tailbase_m = distance_bodypart_bodypart(df = data, bodypart_1="f_snout", bodypart_2="m_tailbase")
    dist_snout_m_tailbase_f = distance_bodypart_bodypart(df = data, bodypart_1="m_snout", bodypart_2="f_tailbase")
    snout_f = data["f_snout_x"]
    snout_m =  data["m_snout_x"]

    face_invest = np.zeros(len(dist_snout_snout))
    body_invest = np.zeros(len(dist_snout_snout))
    ass_invest = np.zeros(len(dist_snout_snout))
    nan_values_f = np.zeros(len(dist_snout_snout))
    nan_values_m = np.zeros(len(dist_snout_snout))

    for i in range(len(dist_snout_snout)):
        if dist_snout_snout[i] <= dist_face:
            face_invest[i] = 1
            
        if dist_snout_f_lateral_l_m[i] <=dist_body or dist_snout_f_lateral_r_m[i] <= dist_body or dist_snout_m_lateral_l_f[i] <= dist_body or dist_snout_m_lateral_r_f[i] <= dist_body:
            body_invest[i] = 1
            
        if dist_snout_f_tailbase_m[i] <=dist_body or dist_snout_m_tailbase_f[i] <=dist_body:
            ass_invest[i] = 1


    social_behavior = {"face investigation": face_invest,
                    "body investigation": body_invest,
                    "anogenital investigation": ass_invest,
                    }
        

    output_df = pd.DataFrame(social_behavior)

    output_df.to_csv(file + f"social_behavior_{dist_face}_{dist_body}_{dist_anogenital}.csv")

