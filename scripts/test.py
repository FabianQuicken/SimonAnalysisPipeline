
import glob
from configurations import mice, paradigms, networks, cameras
import pandas as pd

from get_metadata import get_metadata
from save_metadata_in_df import save_metadata_in_df
from get_bodyparts_from_DLC import rewrite_dataframe, get_bodypart
from likelihood_filter import likelihood_filtering


path = "C:/Code/SimonAnalysisPipeline/raw/*"
file_list = glob.glob(path)
print(file_list)

"""
for file in file_list:
    print(save_metadata_in_df(get_metadata(file)))
"""

df = rewrite_dataframe(csv_file_path=file_list[0])

metadata = get_metadata(csv_file_path=file_list[0])

metadata = save_metadata_in_df(metadata)
#metadata = metadata.T
#print(metadata)
#metadata = metadata.rename(columns={0:"Metadata"})
print(metadata)

new_df = get_bodypart(df_all_bp=df, bodypart="left_ear")

new_df = likelihood_filtering(df=new_df, likelihood_row_name="left_ear_likelihood", filter_val=0.95)

#df1 = pd.DataFrame({"likelihood":[0.99,0.98,0.93,0.94,0.96,0.95]})
#df1_filtered = likelihood_filtering(df=df1)
#print(df1)
#print(df1_filtered)


   
    



