import pandas as pd


def metadata_bodyparts_to_csv(metadata_df,bodyparts_df,path=str):
   # bodyparts_df_length = len(bodyparts_df["left_ear_y"])
    #print(bodyparts_df_length)
    #concat_df = pd.concat([metadata_df,bodyparts_df], axis=0)
    bodyparts_df.to_csv(path)
    #print(concat_df)