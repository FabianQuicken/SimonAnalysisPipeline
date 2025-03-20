# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 08:20:54 2024

@author: fabia
"""

#DLC likelihood filtering

import pandas as pd
import numpy as np


# use this most of the time:

def likelihood_filtering_nans(df, likelihood_row_name=str, filter_val=0.7):
    """
    DeepLabCut provides a likelihood for the prediction of 
    each bodypart in each frame to be correct. Filtering predictions
    for the likelihood, replaces values in the entire row with NaN where the likelihood is below the filter_val.
    """
    df_filtered = df.copy()  # Make a copy to avoid modifying the original DataFrame
    filtered_rows = df_filtered[likelihood_row_name] < filter_val
    df_filtered.loc[filtered_rows] = np.nan
    num_replaced = filtered_rows.sum()
    print(f"The filter replaced values in {num_replaced} rows with NaN out of a total of {len(df)} rows.")
    return df_filtered

# use this only if the data doesn't go to a dataframe: 

def likelihood_filtering(df, likelihood_row_name=str, filter_val = 0.7):
    """
    DeepLabCut provides a likelihood for the prediction of 
    each bodypart in each frame to be correct. Filtering predictions
    for the likelihood, reduces false predictions in the dataset.
    """
    df_filtered = df.copy()
    df_filtered = df[df[likelihood_row_name] > filter_val]
    df_removed_rows = df[df[likelihood_row_name] < filter_val]
    print(f"The filter removed {len(df_removed_rows)} rows of a total of {len(df)} rows.")
    return df_filtered
    


                   