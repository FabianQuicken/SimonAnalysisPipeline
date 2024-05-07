import pandas as pd
from get_metadata import get_metadata

def find_parameter_file(deg_file=str, metadata_dic=dict, parameter_paths=list):
    """
    Compares the metadata of the selected DeepEthogram csv file and compares it to existing parameter files metadata.
    If it finds a file with a matching date, mouse and paradigm, the parameters df gets read and returned.
    """
    for path in parameter_paths:
        parameter_metadata = get_metadata(path)
        print(f"para metadata: {parameter_metadata}")
        print(f"metadata_dic: {metadata_dic}")
        try:
            if metadata_dic["date"] == parameter_metadata["date"] and metadata_dic["mouse"] == parameter_metadata["mouse"] and metadata_dic["paradigm"] == parameter_metadata["paradigm"]:
                print("\nParameter file found!")
                df = pd.read_csv(path, index_col=0)
                return df, path
            else:
                print("No match")
        except:
            print(f"\nNo corresponding parameter file found for file: {deg_file}.")
            

