import pandas as pd
import os

def change_dlc_name(csv_file_path, first_half=False, second_half=False):
    file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    parts = file_name.split('_')
    first_half_name = parts[0] + '_' +  parts[1] + '_' +  parts[2] + '_' +  parts[3] 
    second_half_name = parts[4] + '_' +  parts[5] + '_' +  parts[6] + '_' +  parts[7] + '_' +  parts[8] + '_' +  parts[9]
    if first_half:
        insert = "_Habituation_"
        print(first_half_name, insert, second_half_name)
        new_name = first_half_name + insert + second_half_name
    if second_half:
        insert = "_Experiment_"
        new_name = first_half_name + insert + second_half_name
    return new_name

def change_deg_name(csv_file_path, first_half=False, second_half=False):
    file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    parts = file_name.split('_')
    first_half_name = parts[0] + '_' + parts[1] + '_' +  parts[2] + '_' +  parts[3] 
    second_half_name = parts[4] + '_' +  parts[5]
    if first_half:
        insert = "_Habituation_"
        new_name = first_half_name + insert + second_half_name
    if second_half:
        insert = "_Experiment_"
        new_name = first_half_name + insert + second_half_name
    return new_name


def split_csv(input_file, output_path, dlc = False, deg = False):
    # Read the entire CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    # Extract the first 3 rows as header
    if dlc:
        header_rows = df.iloc[:3]
        # Determine the number of data rows (excluding the header rows)
        num_data_rows = df.shape[0] - 3
    
        # Split the data rows into two parts
        if num_data_rows % 2 == 0:
            split_index = num_data_rows // 2  # even split
        else:
            split_index = num_data_rows // 2 + 1  # uneven split
        
        # First half of data (including header)
        first_half = pd.concat([header_rows, df.iloc[3:3 + split_index]])
        output_name_hab = change_dlc_name(csv_file_path=input_file, first_half=True)
        
        # Second half of data (including header)
        second_half = pd.concat([header_rows, df.iloc[3 + split_index:]])
        output_name_exp = change_dlc_name(csv_file_path=input_file, second_half=True)
        
        # Write the first half to the first output file
        first_half.to_csv(output_path + output_name_hab+".csv", index=False)
        
        # Write the second half to the second output file
        second_half.to_csv(output_path + output_name_exp+".csv", index=False)
    
    if deg:
        header_rows = df.iloc[:1]
        # Determine the number of data rows (excluding the header rows)
        num_data_rows = df.shape[0] - 1
    
        # Split the data rows into two parts
        if num_data_rows % 2 == 0:
            split_index = num_data_rows // 2  # even split
        else:
            split_index = num_data_rows // 2 + 1  # uneven split
        
        # First half of data (including header)
        first_half = pd.concat([header_rows, df.iloc[1:1 + split_index]])
        output_name_hab = change_deg_name(csv_file_path=input_file, first_half=True)
        
        # Second half of data (including header)
        second_half = pd.concat([header_rows, df.iloc[1 + split_index:]])
        output_name_exp = change_deg_name(csv_file_path=input_file, second_half=True)
        
        # Write the first half to the first output file
        first_half.to_csv(output_path + output_name_hab+".csv", index=False)
        
        # Write the second half to the second output file
        second_half.to_csv(output_path + output_name_exp+".csv", index=False)

def split_csv_chatgpt(input_file, output_path, dlc=False, deg=False):
    # Read the entire CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    # Extract the header rows
    if dlc:
        header_rows = df.iloc[:2]
    elif deg:
        header_rows = df.iloc[:0]
    else:
        return  # No valid mode specified
    
    # Determine the number of data rows (excluding the header rows)
    num_data_rows = df.shape[0] - len(header_rows)
    
    # Split the data rows into two parts
    if num_data_rows % 2 == 0:
        split_index = num_data_rows // 2  # even split
    else:
        split_index = num_data_rows // 2 + 1  # uneven split
    
    # First half of data (including header)
    first_half = pd.concat([header_rows, df.iloc[len(header_rows):len(header_rows) + split_index]])
    
    # Second half of data (including header with adjusted index)
    second_half = pd.concat([header_rows, df.iloc[len(header_rows) + split_index - 1:]])
    
    # Reset index for the second half to start from zero
    second_half.reset_index(drop=True, inplace=True)
    
    # Generate output filenames based on mode
    if dlc:
        output_name_hab = change_dlc_name(csv_file_path=input_file, first_half=True)
        output_name_exp = change_dlc_name(csv_file_path=input_file, second_half=True)
    elif deg:
        output_name_hab = change_deg_name(csv_file_path=input_file, first_half=True)
        output_name_exp = change_deg_name(csv_file_path=input_file, second_half=True)
    else:
        return  # No valid mode specified
    
    # Write the first half to the first output file
    first_half.to_csv(os.path.join(output_path, output_name_hab + ".csv"), index=False)
    
    # Write the second half to the second output file
    second_half.to_csv(os.path.join(output_path, output_name_exp + ".csv"), index=False)

