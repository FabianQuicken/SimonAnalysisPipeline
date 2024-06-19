import glob
import pandas as pd

# Define the project path and the pattern to match the CSV files
project_path = "./isot/Odor Investigation/Evaluation"
dlc_raw_path = f"{project_path}/dist_thresh/*.csv"

# Get a list of all CSV files matching the pattern
csv_files = glob.glob(dlc_raw_path)

# Function to interpolate missing values in a DataFrame based on likelihood
def interpolate_dlc_data(file_path, likelihood_threshold=0.6):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Identify coordinate columns (excluding likelihood columns)
    coordinate_columns = [col for col in data.columns if '_x' in col or '_y' in col]
    
    # Identify likelihood columns
    likelihood_columns = [col for col in data.columns if '_likelihood' in col]
    
    # Iterate over each set of coordinates and their corresponding likelihoods
    for coord_col in coordinate_columns:
        # Determine the corresponding likelihood column
        part_name = coord_col.rsplit('_', 1)[0]
        likelihood_col = f"{part_name}_likelihood"
        
        if likelihood_col in data.columns:
            # Mask values below the likelihood threshold
            data.loc[data[likelihood_col] < likelihood_threshold, coord_col] = pd.NA
            
    # Apply linear interpolation for each coordinate column
    data[coordinate_columns] = data[coordinate_columns].interpolate(method='linear', limit_direction='both')
    
    # Return the interpolated DataFrame
    return data

# Process each CSV file
for file_path in csv_files:
    # Interpolate missing values
    interpolated_data = interpolate_dlc_data(file_path)

    # Define the output file path
    output_file_path = file_path.replace('raw', 'interpolated')
    
    # Save the interpolated data to a new CSV file
    interpolated_data.to_csv(output_file_path, index=False)
