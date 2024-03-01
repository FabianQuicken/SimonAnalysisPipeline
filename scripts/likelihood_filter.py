# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 08:20:54 2024

@author: fabia
"""

#DLC likelihood filtering

import pandas as pd

def likelihood_filtering(df, likelihood_row_name = "likelihood", filter_val = 0.95):
    """
    DeepLabCut provides a likelihood for the prediction of 
    each bodypart in each frame to be correct. Filtering predictions
    for the likelihood, reduces false predictions in the dataset.
    """
    df_filtered = df[df[likelihood_row_name] > filter_val]
    df_removed_rows = df[df[likelihood_row_name] < filter_val]
    print(f"The filter removed {len(df_removed_rows)} rows of a total of {len(df)} rows.")
    return df_filtered
    


                   