import pandas as pd

def save_metadata_in_df(metadata_dic):
    """
    transforms a dictionary to a dataframe
    transposes the dataframe to return 
    a one column dataframe containing the metadata
    """
    df = pd.DataFrame(data=metadata_dic)
    #df = df.T
    #df = df.rename(columns={0:"metadata"})
    return df
