import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec

# overlayed event plot
project_path = "./isot/Odor Investigation/Evaluation"

path_asoid = f"{project_path}/asoid_predictions/*.csv"
path_gt = f"{project_path}/ground_truth/*.csv"
file_list_asoid = glob.glob(path_asoid)
file_list_gt = glob.glob(path_gt)

sum_overlay_gt_asoid = []
sum_asoid_fp = []
sum_asoid_fn = []

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
    df_asoid = pd.read_csv(file_list_asoid[i])

    array_gt = df_gt["rightsniffing"].to_numpy()
    array_asoid = df_asoid["rightsniffing"].to_numpy()

    sum_behavior += sum(array_gt)
    sum_frames += len(array_gt) 
    
    array_overlay_gt_asoid = np.zeros(len(array_gt))
    array_asoid_fp = np.zeros(len(array_asoid))
    array_asoid_fn = np.zeros(len(array_asoid))

    for j in range(len(array_gt)):
        # get deg true positives (visualize overlay with ground truth)
        if array_gt[j] == 1 and array_asoid[j] == 1:
            array_overlay_gt_asoid[j] = 1
        

        # get deg false positives
        if array_gt[j] == 0 and array_asoid[j] == 1:
            array_asoid_fp[j] = 1
        

        # get deg false negatives
        if array_gt[j] == 1 and array_asoid[j] == 0:
            array_asoid_fn[j] = 1
    
    precision = sum(array_overlay_gt_asoid) / (sum(array_overlay_gt_asoid) + sum(array_asoid_fp))
    recall = sum(array_overlay_gt_asoid) / (sum(array_overlay_gt_asoid) + sum(array_asoid_fn))
    f1_score = (2 * precision * recall) / (precision + recall)

    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1_score)

    array_overlay_gt_asoid = array_overlay_gt_asoid[0:frames]
    array_asoid_fp = array_asoid_fp[0:frames]
    array_asoid_fn =  array_asoid_fn[0:frames]
    
    sum_overlay_gt_asoid.append(np.where(array_overlay_gt_asoid == 1)[0][::step_size_tp])
    sum_asoid_fp.append(np.where(array_asoid_fp == 1)[0][::step_size])
    sum_asoid_fn.append(np.where(array_asoid_fn == 1)[0][::step_size])

print(precision_list)
print(recall_list)
print(f1_list)


fig = plt.figure(figsize=(15, 5))  # Overall figure size

# Create a gridspec with 2 columns of different widths
gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 1])  # Make event plot 3 times wider than bar plot

# Plot the event plot
ax0 = plt.subplot(gs[0])
for i, array in enumerate(sum_overlay_gt_asoid):
    ax0.vlines(x=array, ymin=i, ymax=(i+1), color="magenta", linestyle='-', alpha=0.7, linewidth=line_width)
for i, array in enumerate(sum_asoid_fn):
    ax0.vlines(x=array, ymin=i, ymax=(i+1), color="yellow", linestyle='-', alpha=0.7, linewidth=line_width)
for i, array in enumerate(sum_asoid_fp):
    ax0.vlines(x=array, ymin=i, ymax=(i+1), color="cyan", linestyle='-', alpha=0.7, linewidth=line_width)


ax0.set_facecolor('black')
ax0.set_xlabel("Frames")
ax0.set_ylabel("Sequences")
ax0.spines['bottom'].set_color('white')
ax0.spines['left'].set_color('white')
ax0.xaxis.label.set_color('white')
ax0.yaxis.label.set_color('white')
ax0.tick_params(axis='x', colors='white')
ax0.tick_params(axis='y', colors='white')
ax0.set_title("A-Soid odor investigation", color='white')

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
ax1.bar(bar_positions, averages, bar_width, color=colors, alpha=0.7)

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
ax1.set_title("A-Soid performance", color='white')

ax2 = plt.subplot(gs[2])

other = sum_frames - sum_behavior

# Create pie chart
wedges, texts, autotexts = ax2.pie(
    [other, sum_behavior], 
    explode=(0.01, 0.01), 
    labels=["Other", "Odor Investigation"], 
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

plt.savefig(f"{project_path}/asoid_ethograms_skip_stepsizetp{step_size_tp}_stepsize{step_size}_frames{frames}.svg", format='svg', facecolor="black")
plt.show()
