import pandas as pd

def save_metadata_in_df(metadata_dic):
    """
    transforms a dictionary to a dataframe
    """
    df = pd.DataFrame(data=metadata_dic)
    return df