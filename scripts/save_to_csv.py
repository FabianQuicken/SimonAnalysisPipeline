import pandas as pd


def metadata_bodyparts_to_csv(metadata_dic,bodyparts_df,path=str):
   # bodyparts_df_length = len(bodyparts_df["left_ear_y"])
    #print(bodyparts_df_length)
    #concat_df = pd.concat([metadata_df,bodyparts_df], axis=0)
    date = metadata_dic["date"]
    mouse = metadata_dic["mouse"]
    paradigm = metadata_dic["paradigm"]
    camera = metadata_dic["camera"]
    bodyparts_df.to_csv(path+date+"_"+camera+mouse+"_"+paradigm+"_bodyparts.csv")
    #print(concat_df)

def parameters_to_csv(metadata_dic, parameters=dict, path=str):
    parameters_df = pd.DataFrame(data=parameters)
    date = metadata_dic["date"]
    mouse = metadata_dic["mouse"]
    paradigm = metadata_dic["paradigm"]
    camera = metadata_dic["camera"]
    parameters_df.to_csv(path+date+"_"+camera+"_"+mouse+"_"+paradigm+"_processed.csv")
    