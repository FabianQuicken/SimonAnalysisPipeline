import glob
import pandas as pd

# Define the project path and the pattern to match the CSV files
project_path = "./isot/Social Investigation/Evaluation"
dlc_raw_path = f"{project_path}/linear_interpolation/raw/*.csv"

# Get a list of all CSV files matching the pattern
csv_files = glob.glob(dlc_raw_path)


# Function to interpolate missing values in a DataFrame
def interpolate_dlc_data(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)

    
    # Identify coordinate columns (excluding likelihood columns)
    coordinate_columns = [col for col in data.columns if '_x' in col or '_y' in col]

    
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