import numpy as np
import pandas as pd
import glob
from scipy.interpolate import interp1d

def polynomial_interpolation(file_path, order=2):
    data = pd.read_csv(file_path)
    coordinate_columns = [col for col in data.columns if '_x' in col or '_y' in col]
    for coord_col in coordinate_columns:
        # Mask values with low likelihood
        part_name = coord_col.rsplit('_', 1)[0]
        likelihood_col = f"{part_name}_likelihood"
        mask = data[likelihood_col] < 0.6
        
        # Interpolate using polynomial
        data.loc[mask, coord_col] = np.nan
        x = np.arange(len(data))
        y = data[coord_col]
        not_nan = ~np.isnan(y)
        interp_func = interp1d(x[not_nan], y[not_nan], kind='quadratic', fill_value='extrapolate')
        data[coord_col] = interp_func(x)
    return data

# Define the project path and the pattern to match the CSV files
project_path = "./isot/Social Investigation/Evaluation"
dlc_raw_path = f"{project_path}/polynomal_interpolation/raw/*.csv"

# Get a list of all CSV files matching the pattern
csv_files = glob.glob(dlc_raw_path)


# Process each CSV file
for file_path in csv_files:
    # Interpolate missing values
    interpolated_data = polynomial_interpolation(file_path)

    # Define the output file path
    output_file_path = file_path.replace('raw', 'interpolated')
    
    # Save the interpolated data to a new CSV file
    interpolated_data.to_csv(output_file_path, index=False)