import numpy as np
import pandas as pd
import glob
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Paths to the prediction and ground truth CSV files
project_path = "./isot/Social Investigation/Evaluation"
path_pred = f"{project_path}/linear_interpolation/interpolated/behavior/*.csv"
path_gt = f"{project_path}/gt/*.csv"

# Collect file paths
file_list_pred = glob.glob(path_pred)
file_list_gt = glob.glob(path_gt)


# Initialize lists to collect all predictions and ground truth values
all_predictions_face = []
all_gt_face = []
all_predictions_body = []
all_gt_body = []
all_predictions_ass = []
all_gt_ass = []

# Read and collect data from each pair of prediction and ground truth files
for pred_file, gt_file in zip(file_list_pred, file_list_gt):
    # Read the CSV files
    df_pred = pd.read_csv(pred_file)
    df_gt = pd.read_csv(gt_file)

    # Extract the arrays
    predictions_face = np.nan_to_num(df_pred["face investigation"].to_numpy())
    ground_truth_face = df_gt["nose-nose"].to_numpy()
    predictions_body = np.nan_to_num(df_pred["body investigation"].to_numpy())
    ground_truth_body = df_gt["nose-body"].to_numpy()
    predictions_ass = np.nan_to_num(df_pred["anogenital investigation"].to_numpy())
    ground_truth_ass = df_gt["nose-anogenital"].to_numpy()

    for i in range(len(ground_truth_face)):
        if ground_truth_face[i] == 1:
            ground_truth_body[i] = 0
            ground_truth_ass[i] = 0
        if ground_truth_body[i] == 1:
            ground_truth_face[i] = 0
            ground_truth_ass[i] = 0
        if ground_truth_ass[i] == 1:
            ground_truth_face[i] = 0
            ground_truth_body[i] = 0

    for i in range(len(predictions_face)):
        if predictions_face[i] == 1:
            predictions_body[i] = 0
            predictions_ass[i] = 0
        if predictions_body[i] == 1:
            predictions_face[i] = 0
            predictions_ass[i] = 0
        if predictions_ass[i] == 1:
            predictions_face[i] = 0
            predictions_body[i] = 0

    # Append the data to the lists
    all_predictions_face.extend(predictions_face)
    all_gt_face.extend(ground_truth_face)
    all_predictions_body.extend(predictions_body)
    all_gt_body.extend(ground_truth_body)
    all_predictions_ass.extend(predictions_ass)
    all_gt_ass.extend(ground_truth_ass)

# Convert lists to numpy arrays
all_predictions_face = np.array(all_predictions_face)

all_gt_face = np.array(all_gt_face)

all_predictions_body = np.array(all_predictions_body)

all_gt_body = np.array(all_gt_body)

all_predictions_ass = np.array(all_predictions_ass)

all_gt_ass = np.array(all_gt_ass)




# Combine the behaviors into a single array for multi-class confusion matrix
# each behavior gets associated to a numerical code (3 for face, 2 for body, 1 for anogenital)
all_predictions = 3 * all_predictions_face + 2 * all_predictions_body + all_predictions_ass
all_ground_truth = 3 * all_gt_face + 2 * all_gt_body + all_gt_ass

# Compute the confusion matrix
conf_matrix = confusion_matrix(all_ground_truth, all_predictions)



# Normalize the confusion matrix by the total number of frames for each class
conf_matrix_normalized = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]


# Define labels for multi-class confusion matrix
labels = ['background behavior', 'face-anogenital', 'nose-body', 'nose-nose']

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

plt.savefig(f"{project_path}/dlc_interpolated_confusionmatrix.svg", format='svg', facecolor="black")
plt.show()
