import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec

# overlayed event plot
project_path = "./isot/Social Investigation/Evaluation"

path_deg = f"{project_path}/linear_interpolation/interpolated/behavior/*.csv"
path_gt = f"{project_path}/gt/*.csv"
file_list_deg = glob.glob(path_deg)
file_list_gt = glob.glob(path_gt)

behavior = "nose"
behavior_net = "face investigation"
network = "DeepLabCut"


sum_overlay_gt_deg = []
sum_deg_fp = []
sum_deg_fn = []

sum_behavior = 0
sum_frames = 0

precision_list = []
recall_list = []
f1_list = []

# Define the step size
step_size_tp = 2
step_size = 1
frames = 10000
line_width = 0.2

for i in range(len(file_list_gt)):
    df_gt = pd.read_csv(file_list_gt[i])
    df_deg = pd.read_csv(file_list_deg[i])

    array_gt = df_gt[f"nose-{behavior}"].to_numpy()
    array_deg = df_deg[f"{behavior_net}"].to_numpy()

    sum_behavior += sum(array_gt)
    sum_frames += len(array_gt) 
    
    array_overlay_gt_deg = np.zeros(len(array_gt))
    array_deg_fp = np.zeros(len(array_deg))
    array_deg_fn = np.zeros(len(array_deg))

    for j in range(len(array_gt)):
        # get deg true positives (visualize overlay with ground truth)
        if array_gt[j] == 1 and array_deg[j] == 1:
            array_overlay_gt_deg[j] = 1
        

        # get deg false positives
        if array_gt[j] == 0 and array_deg[j] == 1:
            array_deg_fp[j] = 1
        

        # get deg false negatives
        if array_gt[j] == 1 and array_deg[j] == 0:
            array_deg_fn[j] = 1
    
    precision = sum(array_overlay_gt_deg) / (sum(array_overlay_gt_deg) + sum(array_deg_fp))
    recall = sum(array_overlay_gt_deg) / (sum(array_overlay_gt_deg) + sum(array_deg_fn))
    f1_score = (2 * precision * recall) / (precision + recall)

    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1_score)

    array_overlay_gt_deg = array_overlay_gt_deg[0:frames]
    array_deg_fp = array_deg_fp[0:frames]
    array_deg_fn =  array_deg_fn[0:frames]
    
    sum_overlay_gt_deg.append(np.where(array_overlay_gt_deg == 1)[0][::step_size_tp])
    sum_deg_fp.append(np.where(array_deg_fp == 1)[0][::step_size])
    sum_deg_fn.append(np.where(array_deg_fn == 1)[0][::step_size])

print(precision_list)
print(recall_list)
print(f1_list)


fig = plt.figure(figsize=(15, 5))  # Overall figure size

# Create a gridspec with 2 columns of different widths
gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 1])  # Make event plot 3 times wider than bar plot

# Plot the event plot
ax0 = plt.subplot(gs[0])

for i, array in enumerate(sum_deg_fn):
    ax0.vlines(x=array, ymin=i, ymax=i+1, color="yellow", linestyle='-', alpha=0.7, linewidth=line_width)
for i, array in enumerate(sum_deg_fp):
    ax0.vlines(x=array, ymin=i, ymax=i+1, color="cyan", linestyle='-', alpha=0.7, linewidth=line_width)
for i, array in enumerate(sum_overlay_gt_deg):
    ax0.vlines(x=array, ymin=i, ymax=i+1, color="magenta", linestyle='-', alpha=0.7, linewidth=line_width)


ax0.set_facecolor('black')
ax0.set_xlabel("Frames")
ax0.set_ylabel("Sequences")
ax0.spines['bottom'].set_color('white')
ax0.spines['left'].set_color('white')
ax0.xaxis.label.set_color('white')
ax0.yaxis.label.set_color('white')
ax0.tick_params(axis='x', colors='white')
ax0.tick_params(axis='y', colors='white')
ax0.set_title(f"{network} {behavior} investigation", color='white')

# Compute averages
avg_precision = np.mean(precision_list)
avg_recall = np.mean(recall_list)
avg_f1 = np.mean(f1_list)

# Plot bar plot with scatter overlay
ax1 = plt.subplot(gs[1])
categories = ['Precision', 'Recall', 'F1 Score']
averages = [avg_precision, avg_recall, avg_f1]
all_values = [precision_list, recall_list, f1_list]

# Plot bars
bar_width = 0.4
bar_positions = np.arange(len(categories))
colors = ['cyan', 'yellow', 'magenta']
ax1.bar(bar_positions, averages, bar_width, color=colors, alpha=0.6)

# Overlay scatter plot
for i, values in enumerate(all_values):
    ax1.scatter([bar_positions[i]] * len(values), values, color=colors[i])

# Add labels, title, and format axes
ax1.set_xticks(bar_positions)
ax1.set_yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
ax1.set_xticklabels(categories)
ax1.set_xlabel("Metrics")
ax1.set_ylabel("Scores")
ax1.set_title("Precision, Recall, F1 Score with Scatter Overlay")

# Change background and axis colors
ax1.set_facecolor('black')
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.xaxis.label.set_color('white')
ax1.yaxis.label.set_color('white')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.set_title(f"{network} performance", color='white')

ax2 = plt.subplot(gs[2])

other = sum_frames - sum_behavior

# Create pie chart
wedges, texts, autotexts = ax2.pie(
    [other, sum_behavior], 
    explode=(0.01, 0.01), 
    labels=["Other", f"{behavior} Investigation"], 
    autopct=lambda p: f'{int(p * other / 100)}', 
    colors=["silver", "white"], 
    startangle=90
)

# Set the face color of the pie chart
ax2.set_facecolor('black')

# Set label colors
for text in texts:
    text.set_color('white')  # Change label color to white

# Set autopct colors (percentage texts inside the pie chart)
for autotext in autotexts:
    autotext.set_color('black')  # Change percentage text color to black

# Add a title
ax2.set_title("Proportion of Frames Containing Behavior", color='white')

plt.tight_layout()
#plt.show()
plt.savefig(f"{project_path}/{network}_ethograms_{behavior}_investigation_skip_stepsizetp{step_size_tp}_stepsize{step_size}_frames{frames}_70_80_65_linear_interpolated.svg", format='svg', facecolor="black")

