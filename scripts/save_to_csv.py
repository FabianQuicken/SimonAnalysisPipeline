import pandas as pd


def metadata_bodyparts_to_csv(metadata_dic,bodyparts_df,path=str):
    date = metadata_dic["date"]
    mouse = metadata_dic["mouse"]
    paradigm = metadata_dic["paradigm"]
    camera = metadata_dic["camera"]
    bodyparts_df.to_csv(path+date+"_"+camera+mouse+"_"+paradigm+"_bodyparts.csv")


def parameters_to_csv(metadata_dic, parameters=dict, path=str):
    parameters_df = pd.DataFrame(data=parameters)
    date = metadata_dic["date"]
    mouse = metadata_dic["mouse"]
    paradigm = metadata_dic["paradigm"]
    camera = metadata_dic["camera"]
    parameters_df.to_csv(path+date+"_"+camera+"_"+mouse+"_"+paradigm+"_processed.csv")
    
def ini_processed_parameters_df(processed_parameters=dict,metadata_dic=dict):
    date = metadata_dic["date"]
    mouse = metadata_dic["mouse"]
    paradigm = metadata_dic["paradigm"]
    camera = metadata_dic["camera"]
    index_name = date+"_"+camera+"_"+mouse+"_"+paradigm
    p_parameters_df = pd.DataFrame(data=processed_parameters,index=[index_name])
    p_parameters_df.index.name = 'Index'
    return p_parameters_df

def append_processed_parameters_df(processed_parameters_df,processed_parameters=list,metadata_dic=dict):
    date = metadata_dic["date"]
    mouse = metadata_dic["mouse"]
    paradigm = metadata_dic["paradigm"]
    camera = metadata_dic["camera"]
    index_name = date+"_"+camera+"_"+mouse+"_"+paradigm
    processed_parameters_df.loc[index_name] = processed_parameters
    return processed_parameters_df

def processed_bodyparts_to_csv(habituation,p_parameters,path=str):
    if habituation:
        p_parameters.to_csv(path+"habituation_processed_parameters.csv")
    elif not habituation:
        p_parameters.to_csv(path+"experiment_processed_parameters.csv")

def append_to_existing_csv(existing_csv_path, new_df):
    existing_df = pd.read_csv(existing_csv_path, index_col="Index")
    merged_df = pd.concat([existing_df, new_df], axis=0, ignore_index=False)
    merged_df.to_csv(existing_csv_path)


