import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
events1 = np.random.randint(0, 2, size=35296)  # First row of events (0s and 1s)
events2 = np.random.randint(0, 2, size=35296)  # Second row of events (0s and 1s)

# Find the positions of "1" values
positions1 = np.where(events1 == 1)[0]
positions2 = np.where(events2 == 1)[0]

# Create a new figure
plt.figure(figsize=(10, 6))  # Adjust figsize as needed

# Plot the event plot
plt.eventplot(positions1, lineoffsets=0, colors='b', label='Row 1')
plt.eventplot(positions2, lineoffsets=1, colors='r', label='Row 2')

# Add labels and legend
plt.xlabel('Time')
plt.ylabel('Rows')
plt.title('Event Plot with Two Rows')
plt.legend()

# Set x-axis limits to cover the full length of the arrays
plt.xlim(0, len(events1))

# Save the figure as SVG
plt.savefig('event_plot.svg', format='svg')

plt.show()