import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec




gt_path = "./isot/Odor Investigation/Evaluation/training_dataset/deg/*.csv"
csv_files = glob.glob(gt_path)

all_background = 0
all_water = 0
all_stim = 0


for file in csv_files:

    df = pd.read_csv(file)
    copy_df = df.copy()

    background_data = copy_df["background"]
    water_data = copy_df["leftsniffing"]
    stim_data = copy_df["rightsniffing"]


    all_water += sum(water_data)
    all_stim += sum(stim_data)

    all_background += sum(background_data)

    print(sum(background_data))

# Function to calculate the percentage
def autopct_format(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(pct*total/100.0)
        return f'{val}'
    return my_autopct

plt.figure(figsize=(5,5), facecolor='black')
wedges, texts, autotexts = plt.pie([all_background, all_water, all_stim],
        explode=(0.01, 0.01, 0.01),
        labels=["other","left dish","right dish"],
        autopct=autopct_format([all_background, all_water, all_stim]),
        colors=["silver","lightskyblue","cornsilk"],
        startangle=90,
        pctdistance=0.85,
        labeldistance=1.05)
#plt.gca().set_facecolor('black')

# Set label colors
for text in texts:
    text.set_color('white')  # Change label color to white

# Set autopct colors (percentage texts inside the pie chart)
for autotext in autotexts:
    autotext.set_color('black')  # Change percentage text color to black

ax = plt.gca()
ax.set_title("odor investigation behavior dataset [frames]", color='white')

#plt.savefig(f"./isot/Odor Investigation/Evaluation/odor_investigation_dataset.svg", format='svg', facecolor="black")

plt.show()