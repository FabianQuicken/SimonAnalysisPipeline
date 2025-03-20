import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec
import re
import seaborn as sns


#für face scheint 95 am besten 
#für body 85


# Function to extract the numeric suffix from the file name
def extract_suffix(file_path):
    match = re.search(r'_(\d+)\.csv$', file_path)
    if match:
        return int(match.group(1))
    return -1

# overlayed event plot
project_path = "./isot/Odor Investigation/Evaluation"

path_dlc = f"{project_path}/dist_thresh/mouse_117_interpolated/*.csv"
file_gt = f"{project_path}/ground_truth/240220_side_117_V1_Experiment_Urinright_labels.csv"
file_list_dlc = glob.glob(path_dlc)


# Sorting the file list based on the extracted numeric suffix
sorted_file_list = sorted(file_list_dlc, key=extract_suffix)


"""
# Print the sorted file list
for file in sorted_file_list:
    print(file)
"""

behavior = "water investigation"
behavior_net = "leftsniffing"
network = "DeepLabCut"

precisions = []
recalls = []
f_scores = []
nan_tp_count = []

for i in range(len(sorted_file_list)):
    df_gt = pd.read_csv(file_gt)
    df_dlc = pd.read_csv(sorted_file_list[i])



    array_gt = df_gt["leftsniffing"].to_numpy()
    array_dlc = df_dlc["left investigation"].to_numpy()    

    array_dlc_tp = np.zeros(len(array_gt))
    array_dlc_fp = np.zeros(len(array_dlc))
    array_dlc_fn = np.zeros(len(array_dlc))

    nose_nans = df_dlc["nose nan"]

    nan_tp = 0

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

        # count NaN true positives in ground truth
        if nose_nans[j] == 1 and array_gt[j] == 1:
            nan_tp += 1



    precision = sum(array_dlc_tp) / (sum(array_dlc_tp) + sum(array_dlc_fp))
    recall = sum(array_dlc_tp) / (sum(array_dlc_tp) + sum(array_dlc_fn))
    if recall >= 0.99:
        recall = 0.99
    f1_score = (2 * precision * recall) / (precision + recall)
    nan_tp_rate = nan_tp / (sum(array_dlc_tp) + sum(array_dlc_fn))

    precisions.append(precision)
    recalls.append(recall)
    f_scores.append(f1_score)
    nan_tp_count.append(nan_tp_rate)
    

# Plotting the precision, recall, and F1 score as line graphs
plt.figure(figsize=(5, 5), facecolor='black')
plt.plot(range(len(precisions)), precisions, label='precision', color='cyan')
plt.plot(range(len(recalls)), recalls, label='recall', color='yellow')
plt.plot(range(len(f_scores)), f_scores, label='F1_score', color='magenta')
plt.hlines(y=nan_tp_count[50], xmin=0, xmax=149, colors='grey', linestyles='--', label='fn due to missing prediction')
#plt.plot(range(len(nan_tp_count)), nan_tp_count, label='NaN TP rate', color='grey')
plt.xlabel('distance threshold [pixel]', color='white')
plt.ylabel('score', color='white')
plt.ylim(0, 1)
plt.yticks(np.arange(0, 1.1, 0.2), color='white')
plt.title(f'metrics for water investigation', color='white')
plt.legend()
plt.legend(facecolor='black', edgecolor='white', labelcolor='white')
#plt.grid(True)
sns.despine()
plt.gca().set_facecolor('black')
plt.gca().tick_params(colors='white')
plt.gca().spines['top'].set_color('white')
plt.gca().spines['bottom'].set_color('white')
plt.gca().spines['left'].set_color('white')
plt.gca().spines['right'].set_color('white')
plt.savefig(f"{project_path}/{behavior}_mouse_117_interpolated.svg", format='svg', facecolor="black")
plt.show()
