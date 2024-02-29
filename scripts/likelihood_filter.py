# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 08:20:54 2024

@author: fabia
"""

#DLC likelihood filtering

import pandas as pd

def likelihood_filtering(df, filter_val = 0.95):
    """
    DeepLabCut provides a likelihood for the prediction of 
    each bodypart in each frame to be correct. Filtering predictions
    for the likelihood, reduces false predictions in the dataset.
    """
    df_filtered = df[df["likelihood"] > 0.95]
    df_removed_rows = df[df["likelihood"] < 0.95]
    print(f"The filter removed {len(df_removed_rows)} rows of a total of {len(df)} rows.")
    return df_filtered
    

df1 = pd.DataFrame({"likelihood":[0.99,0.98,0.93,0.94,0.96,0.95]})
df1_filtered = likelihood_filtering(df=df1)
print(df1)
print(df1_filtered)
                   