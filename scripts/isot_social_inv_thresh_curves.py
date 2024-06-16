import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec
import re


#für face scheint 95 am besten 
#für body 85


# Function to extract the numeric suffix from the file name
def extract_suffix(file_path):
    match = re.search(r'_(\d+)\.csv$', file_path)
    if match:
        return int(match.group(1))
    return -1

# overlayed event plot
project_path = "./isot/Social Investigation/Evaluation"

path_dlc = f"{project_path}/dlc_raw/39804_39839_distance_threshs/*.csv"
file_gt = f"{project_path}/gt/221205_topview_r39804_i39839_experiment_labels.csv"
file_list_dlc = glob.glob(path_dlc)

# Sorting the file list based on the extracted numeric suffix
sorted_file_list = sorted(file_list_dlc, key=extract_suffix)

"""
# Print the sorted file list
for file in sorted_file_list:
    print(file)
"""

behavior = "anogenital"
behavior_net = "anogenital investigation"
network = "DeepLabCut"

precisions = []
recalls = []
f_scores = []

for i in range(len(sorted_file_list)):
    df_gt = pd.read_csv(file_gt)
    df_dlc = pd.read_csv(sorted_file_list[i])

    array_gt = df_gt[f"nose-{behavior}"].to_numpy()
    array_dlc = df_dlc[f"{behavior_net}"].to_numpy()    

    array_dlc_tp = np.zeros(len(array_gt))
    array_dlc_fp = np.zeros(len(array_dlc))
    array_dlc_fn = np.zeros(len(array_dlc))

    for j in range(len(array_gt)):
        # get dlc true positives (visualize overlay with ground truth)
        if array_gt[j] == 1 and array_dlc[j] == 1:
            array_dlc_tp[j] = 1
        

        # get dlc false positives
        if array_gt[j] == 0 and array_dlc[j] == 1:
            array_dlc_fp[j] = 1
        

        # get dlc false negatives
        if array_gt[j] == 1 and array_dlc[j] == 0:
            array_dlc_fn[j] = 1



    precision = sum(array_dlc_tp) / (sum(array_dlc_tp) + sum(array_dlc_fp))
    recall = sum(array_dlc_tp) / (sum(array_dlc_tp) + sum(array_dlc_fn))
    f1_score = (2 * precision * recall) / (precision + recall)

    precisions.append(precision)
    recalls.append(recall)
    f_scores.append(f1_score)


# Plotting the precision and recall as line graphs
plt.figure(figsize=(10, 6))
plt.plot(range(len(precisions)), precisions, label='Precision', marker='o')
plt.plot(range(len(recalls)), recalls, label='Recall', marker='o')
plt.plot(range(len(f_scores)), f_scores, label='F1_score', marker='o')
plt.xlabel('File Index')
plt.ylabel('Score')
plt.title('Precision and Recall over Different Files')
plt.legend()
plt.grid(True)
plt.savefig(f"{project_path}/{behavior}_39804_39839.svg", format='svg', facecolor="white")
plt.show()
