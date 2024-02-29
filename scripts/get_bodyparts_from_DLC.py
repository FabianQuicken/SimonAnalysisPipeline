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
    """
    df = pd.read_csv(csv_file_path)
    df = df.iloc[4:]
    new_df = pd.DataFrame(columns = dlc_petridish_layout)
    print(new_df)
    new_df.concatinate(df)
    print(new_df)
    return new_df
    
    
    