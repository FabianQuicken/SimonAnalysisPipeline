import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

#project_path = "./datasets/testing"
project_path = "D:/Eventplots/speedometer"
#file_path = "/processed/parameters/done/240220_top_1_V1_Experiment_Urinright_processed.csv"
file_path = "D:/Eventplots/speedometer/240220_top_1_V1_Experiment_Urinright_processed.csv"
df = pd.read_csv(file_path)

speed_values = df["speed_in_km/h"]
speed_values = np.array(speed_values).astype(float)
speed_values = np.nan_to_num(speed_values, nan=0.0)
speed_values = speed_values * 1000
speed_values = speed_values.round()

speed_values = speed_values / 11.1111

speed_values = speed_values.astype(int)

skip_frames = 1
speed_values = speed_values[::skip_frames]
print(min(speed_values))

print(max(speed_values))
for i in range(len(speed_values)):
    if speed_values[i] > 360:
        speed_values[i] = 360

# Normalize speed values to range 0 to 100
min_speed = np.min(speed_values)
max_speed = np.max(speed_values)
normalized_speeds = 100 * (speed_values - min_speed) / (max_speed - min_speed)

# Set up the figure and axis
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')  # Set figure background to black
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('black')  # Set axis background to black

# Create the speedometer arc (full circle)
theta = np.linspace(0, 2 * np.pi, 100)  # Full circle
x = np.cos(theta)
y = np.sin(theta)
ax.plot(x, y, color='white')  # Circle outline in white

# Fill the circle inside with black
ax.fill(x, y, 'black')

# Add value ticks around the circle
num_ticks = 20  # Number of ticks to display
tick_angles = np.linspace(0, 2 * np.pi, num_ticks, endpoint=False)
tick_length = 0.05  # Length of each tick
for i, angle in enumerate(tick_angles):
    # Adjust the angle to move clockwise
    adjusted_angle = (1/2 * np.pi) - angle
    x_start, y_start = np.cos(adjusted_angle), np.sin(adjusted_angle)
    x_end, y_end = np.cos(adjusted_angle) * (1 - tick_length), np.sin(adjusted_angle) * (1 - tick_length)
    ax.plot([x_start, x_end], [y_start, y_end], 'white')  # Ticks in white
    # Calculate and add the text for each tick
    tick_value = int(i / num_ticks * max_speed)
    x_text, y_text = np.cos(adjusted_angle) * (1 - tick_length - 0.08), np.sin(adjusted_angle) * (1 - tick_length - 0.08)
    ax.text(x_text, y_text, f'{tick_value}', ha='center', va='center', fontsize=8, color='white')  # Text in white

# Add transparent background for the area between 0 and 100
start_angle = np.pi / 2  # Start from the top (90 degrees)
end_speed = 18  # Speed value at the end of the shaded area
end_angle = start_angle - (end_speed / max_speed * 2 * np.pi)  # Calculate end angle based on the speed value
theta = np.linspace(start_angle, end_angle, 100)
x_fill = np.concatenate([[0], np.cos(theta), [0]])
y_fill = np.concatenate([[0], np.sin(theta), [0]])
ax.fill(x_fill, y_fill, 'cyan', alpha=0.3)

# Needle of the speedometer
needle, = ax.plot([], [], 'r-', linewidth=2)

# Annotation for the speed value
speed_text = ax.text(0, -0.1, '', ha='center', fontsize=12, color='white')  # Speed text in white

# Initialize a list to keep track of the last 100 speed values
last_speeds = []

# Initialize Line2D objects for the history lines
history_lines = [ax.plot([], [], 'r-', alpha=0.1)[0] for _ in range(100)]

def init():
    needle.set_data([], [])
    speed_text.set_text('')
    for line in history_lines:
        line.set_data([], [])
    return needle, speed_text, *history_lines

def update(frame):
    global last_speeds
    
    # Map normalized speed value to angle, starting from top (north) and moving clockwise
    angle = (1/2 * np.pi) - (2 * np.pi * frame / 100)  # Start from top and move clockwise
    needle.set_data([0, np.cos(angle)], [0, np.sin(angle)])
    actual_speed = min_speed + frame * (max_speed - min_speed) / 100
    #speed_text.set_text(f'Speed: {actual_speed:.1f}')

    # Append the current frame to the last_speeds list
    last_speeds.append(frame)
    if len(last_speeds) > 100:
        last_speeds.pop(0)

    # Update the history lines
    for i, past_frame in enumerate(last_speeds):
        past_angle = (1/2 * np.pi) - (2 * np.pi * past_frame / 100)
        history_lines[i].set_data([0, np.cos(past_angle)], [0, np.sin(past_angle)])

    return needle, speed_text, *history_lines

ani = animation.FuncAnimation(fig, update, frames=normalized_speeds, init_func=init, blit=True, repeat=False)

# Save the animation
#ani.save(f'{project_path}/figures/speedometer_animation.mp4', writer='ffmpeg', fps=60/skip_frames)
ani.save(f'{project_path}/speedometer_animation.mp4', writer='ffmpeg', fps=30/skip_frames)

#plt.show()