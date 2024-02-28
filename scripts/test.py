
import glob
from configurations import mice, paradigms, networks, cameras

from get_metadata import get_metadata
from save_metadata_in_df import save_metadata_in_df


path = "C:/Users/Fabian/Code/SimonAnalysisPipeline/raw/*"
file_list = glob.glob(path)

"""
for file in file_list:
    print(save_metadata_in_df(get_metadata(file)))
"""
for file in file_list:
    print(save_metadata_in_df(get_metadata(file)))


#test = get_metadata(csv_file_path="C:/Users/Fabian/Code/SimonAnalysisPipeline/raw/240220_top_105_V1_Habituation_UrinrightDLC_resnet50_DLC1Feb20shuffle1_300000.csv")
#df = save_metadata_in_df(test)
#print(df)
   
    



