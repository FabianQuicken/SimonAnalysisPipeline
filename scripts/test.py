
import glob
from configurations import mice, paradigms, networks, cameras

from get_metadata import get_metadata
from save_metadata_in_df import save_metadata_in_df
from get_bodyparts_from_DLC import rewrite_dataframe


path = "C:/Users/quicken/Code/SimonAnalysisPipeline/raw/*"
file_list = glob.glob(path)
print(file_list)

"""
for file in file_list:
    print(save_metadata_in_df(get_metadata(file)))
"""

df = rewrite_dataframe(csv_file_path=file_list[0])


   
    



