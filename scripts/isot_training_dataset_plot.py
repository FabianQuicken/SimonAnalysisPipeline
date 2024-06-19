import matplotlib.pyplot as plt
import numpy as np

# Data for the plot
values = [282360, 300]
colors = ['grey', 'white']

# Create the plot
fig, ax = plt.subplots()

# Bar plot with specified colors
bars = ax.bar(['DeepEthogram', 'DeepLabCut'], values, color=colors)

# Set logarithmic scale for y-axis starting from 1 (0 is not allowed in log scale)
ax.set_yscale('log')
ax.set_ylim(bottom=1)

# Set the axis and text colors to white
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.yaxis.label.set_color('white')
ax.xaxis.label.set_color('white')

# Set the x-axis and y-axis to white
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Remove top and right spines for better aesthetics
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

# Set the background color to black
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Save the plot as an SVG file
plt.savefig('C:/ISOT 2024/Poster/bar_plot.svg', format='svg', facecolor=fig.get_facecolor())

# Display the plot (optional)
plt.show()