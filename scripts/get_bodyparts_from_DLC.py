# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 07:55:24 2024

@author: fabia
"""
import pandas as pd
from configurations import dlc_petridish_layout

# Script um einzelne Bodyparts aus dlc csv extrahieren zu können

def get_df(csv_file_path):
    """
    This func returns the first row from a DLC output csv as a 
    pandas dataframe. The first row contains the network name.
    """
    df = pd.read_csv(csv_file_path)
    return df

    
def rewrite_dataframe(csv_file_path, df_cols = dlc_petridish_layout):
    """
    This func returns a pandas Dataframe, 
    with an easy to work column layout.
    The information gets changed into floats, because DLC saves it in csv's as strings.
    """
    df = pd.read_csv(csv_file_path,names=df_cols)
    df = df.iloc[3:]
    df = df.astype(float)
    return df

def get_bodypart(df_all_bp, df_spec_bp=pd.DataFrame(), bodypart=str):
    """
    Important: A modified dataframe must be passed to this func, like in rewrite_df().
    Adds bodypart information (bodypart_x, bodypart_y, bodypart_likelihood)
    To another dataframe and returns this dataframe.
    If no output dataframe is provided, an empty one is generated and filled.
    """
    df_spec_bp[bodypart+"_x"] = df_all_bp[bodypart+"_x"]
    df_spec_bp[bodypart+"_y"] = df_all_bp[bodypart+"_y"]
    df_spec_bp[bodypart+"_likelihood"] = df_all_bp[bodypart+"_likelihood"]
    return df_spec_bp
    
    
    