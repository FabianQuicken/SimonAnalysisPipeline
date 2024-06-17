import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from matplotlib import gridspec




gt_path = "./isot/Social Investigation/Evaluation/gt/*.csv"
csv_files = glob.glob(gt_path)

all_background = 0
all_face = 0
all_body = 0
all_anogenital = 0

for file in csv_files:

    df = pd.read_csv(file)
    copy_df = df.copy()

    background_data = copy_df["background"]
    face_data = copy_df["nose-nose"]
    body_data = copy_df["nose-body"]
    anogenital_data = copy_df["nose-anogenital"]

    all_face += sum(face_data)
    all_body += sum(body_data)
    all_anogenital += sum(anogenital_data)
    all_background += sum(background_data)

# Function to calculate the percentage
def autopct_format(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(pct*total/100.0)
        return f'{val}'
    return my_autopct

plt.figure(figsize=(5,5), facecolor='black')
wedges, texts, autotexts = plt.pie([all_background, all_anogenital, all_body, all_face],
        explode=(0.01, 0.01, 0.01, 0.01),
        labels=["other","face","body","anogenital"],
        autopct=autopct_format([all_background, all_anogenital, all_body, all_face]),
        colors=["silver","mistyrose","cornsilk","lavender"],
        startangle=90)
#plt.gca().set_facecolor('black')

# Set label colors
for text in texts:
    text.set_color('white')  # Change label color to white

# Set autopct colors (percentage texts inside the pie chart)
for autotext in autotexts:
    autotext.set_color('black')  # Change percentage text color to black

ax = plt.gca()
ax.set_title("social investigation behavior dataset [frames]", color='white')

#plt.savefig(f"./isot/Social Investigation/Evaluation/social_investigation_dataset.svg", format='svg', facecolor="black")

plt.show()

