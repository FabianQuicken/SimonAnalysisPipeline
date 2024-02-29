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
    df = df.iloc[1:]
    return df

    
def get_bodypart(csv_file_path, bodypart=str):
    """
    This func returns a bodypart as pandas Dataframe, 
    passed as argument (string) from a
    DLC csv file.
    """
    df = get_df(csv_file_path)
    bodypart_df = df[bodypart]
    return bodypart_df
    
    
    