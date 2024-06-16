import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec
import re
from sklearn.metrics import precision_recall_curve, average_precision_score

# Function to extract the numeric suffix from the file name
def extract_suffix(file_path):
    match = re.search(r'_(\d+)\.csv$', file_path)
    if match:
        return int(match.group(1))
    return -1

# Overlayed event plot
project_path = "./isot/Social Investigation/Evaluation"

path_dlc = f"{project_path}/dlc_raw/39804_39839_distance_threshs/*.csv"
file_gt = f"{project_path}/gt/221205_topview_r39804_i39839_experiment_labels.csv"
file_list_dlc = glob.glob(path_dlc)

# Sorting the file list based on the extracted numeric suffix
sorted_file_list = sorted(file_list_dlc, key=extract_suffix)

behavior = "nose"
behavior_net = "face investigation"
network = "DeepLabCut"

all_gt = []
all_scores = []

for i in range(len(sorted_file_list)):
    df_gt = pd.read_csv(file_gt)
    df_dlc = pd.read_csv(sorted_file_list[i])

    array_gt = df_gt[f"nose-{behavior}"].to_numpy()
    array_dlc = df_dlc[f"{behavior_net}"].to_numpy()

    all_gt.extend(array_gt)
    all_scores.extend(array_dlc)

# Convert lists to numpy arrays
all_gt = np.array(all_gt)
all_scores = np.array(all_scores)

# Calculate precision-recall curve
precision, recall, _ = precision_recall_curve(all_gt, all_scores)
average_precision = average_precision_score(all_gt, all_scores)

# Plot the Precision-Recall curve
plt.figure()
plt.step(recall, precision, where='post', color='b', alpha=0.2,
         label=f'Average precision score = {average_precision:.2f}')
plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.show()