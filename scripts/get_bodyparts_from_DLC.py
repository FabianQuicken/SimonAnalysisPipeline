# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 07:55:24 2024

@author: fabia
"""
import pandas as pd

# Script um einzelne Bodyparts aus dlc csv extrahieren zu können

def get_df(csv_file_path):
    """
    This func returns the first row from a DLC output csv as a 
    pandas dataframe. The first row contains the network name.
    """
    df = pd.read_csv(csv_file_path)
    return df

    
def rewrite_dataframe(csv_file_path, df_cols = list):
    """
    This func returns a pandas Dataframe, 
    with an easy to work column layout.
    The information gets changed into floats, because DLC saves it in csv's as strings.
    """
    df = pd.read_csv(csv_file_path,names=df_cols)
    data = df.copy()
    data = data.iloc[3:]
    data = data.astype(float)
    return data

def get_bodypart(df_all_bp, bodypart_list=list):
    """
    Important: A modified dataframe must be passed to this func, like in rewrite_df().
    Adds bodypart information (bodypart_x, bodypart_y, bodypart_likelihood)
    To another dataframe and returns this dataframe.
    If no output dataframe is provided, an empty one is generated and filled.
    """
    data = df_all_bp.copy()
    df_spec_bp = pd.DataFrame()
    df = df_spec_bp.copy()
    for bodypart in bodypart_list:
        df[bodypart+"_x"] = data[bodypart+"_x"]
        df[bodypart+"_y"] = data[bodypart+"_y"]
        df[bodypart+"_likelihood"] = data[bodypart+"_likelihood"]
    return df
    
    