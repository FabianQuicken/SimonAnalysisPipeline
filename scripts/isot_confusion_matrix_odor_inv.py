import numpy as np
import pandas as pd
import glob
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Paths to the prediction and ground truth CSV files
project_path = "./isot/Odor Investigation/Evaluation"
path_asoid = f"{project_path}/dist_thresh/bodyparts_interpolated_60_opt/*.csv"
path_gt = f"{project_path}/ground_truth/*.csv"

# Collect file paths
file_list_asoid = glob.glob(path_asoid)
file_list_gt = glob.glob(path_gt)

# Initialize lists to collect all predictions and ground truth values
all_predictions_right = []
all_ground_truth_right = []
all_predictions_left = []
all_ground_truth_left = []

# Read and collect data from each pair of prediction and ground truth files
for asoid_file, gt_file in zip(file_list_asoid, file_list_gt):
    # Read the CSV files
    df_asoid = pd.read_csv(asoid_file)
    df_gt = pd.read_csv(gt_file)

    # Extract the arrays
    predictions_right = np.nan_to_num(df_asoid["right investigation"].to_numpy())
    ground_truth_right = df_gt["rightsniffing"].to_numpy()
    predictions_left = np.nan_to_num(df_asoid["left investigation"].to_numpy())
    ground_truth_left = df_gt["leftsniffing"].to_numpy()

    for i in range(len(predictions_right)):
        if predictions_right[i] == 1:
            predictions_left[i] = 0
        if predictions_left[i] == 1:
            predictions_right[i] = 0



    # Append the data to the lists
    all_predictions_right.extend(predictions_right)
    all_ground_truth_right.extend(ground_truth_right)
    all_predictions_left.extend(predictions_left)
    all_ground_truth_left.extend(ground_truth_left)

# Convert lists to numpy arrays
all_predictions_right = np.array(all_predictions_right)
all_ground_truth_right = np.array(all_ground_truth_right)
all_predictions_left = np.array(all_predictions_left)
all_ground_truth_left = np.array(all_ground_truth_left)

# Combine the behaviors into a single array for multi-class confusion matrix
all_predictions = 2 * all_predictions_right + all_predictions_left
all_ground_truth = 2 * all_ground_truth_right + all_ground_truth_left

# Compute the confusion matrix
conf_matrix = confusion_matrix(all_ground_truth, all_predictions)


# Normalize the confusion matrix by the total number of frames for each class
conf_matrix_normalized = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]


# Define labels for multi-class confusion matrix
labels = ['background behavior', 'water investigation', 'odor investigation']

# Create a custom colormap from black to yellow
cmap = LinearSegmentedColormap.from_list('grey_to_yellow', ['black', 'gold'], N=256)

# Plot the normalized confusion matrix with raw values as annotations
plt.figure(figsize=(10, 8), facecolor='black')
ax = sns.heatmap(conf_matrix_normalized, annot=conf_matrix.astype(int), fmt='d', cmap=cmap, xticklabels=labels, yticklabels=labels)

# Set the face color of the plot background
ax.set_facecolor('black')

# Set label colors
ax.set_xlabel('predicted', color='white')
ax.set_ylabel('true', color='white')
ax.set_title('DeepLabCut (interpolated) confusion matrix', color='white')

# Set tick colors
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Set tick label colors
plt.setp(ax.get_xticklabels(), color='white')
plt.setp(ax.get_yticklabels(), color='white')

# Customize the colorbar
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(cbar.ax.yaxis.get_majorticklabels(), color='white')
cbar.set_label(label="", color='white')

plt.savefig(f"{project_path}/deeplabcut_interpolated_confusionmatrix.svg", format='svg', facecolor="black")
plt.show()
