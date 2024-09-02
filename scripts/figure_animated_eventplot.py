
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def live_event_plot(csv_files, titles, video_file, output_file, fps=30, num_frames=1300):
    # Load the CSV data for all datasets
    datasets = [pd.read_csv(csv_file) for csv_file in csv_files]
    
    # Extract behavior events from each dataset
    events = []
    for data in datasets:
        leftsniffing = data.index[data['stimulusinvestigation'] == 1].tolist()
        rightsniffing = data.index[data['drinking'] == 1].tolist()
        events.append((leftsniffing, rightsniffing))

    # Load the video
    cap = cv2.VideoCapture(video_file)
    
    # Get video properties
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # New dimensions for video and plot
    plot_height = 200  # Height of the plot
    video_height = original_height - plot_height
    video_width = original_width
    output_height = original_height
    output_width = original_width

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'XVID' or 'MJPG' if 'mp4v' is not working
    out = cv2.VideoWriter(output_file, fourcc, fps, (output_width, output_height))  # Extra space for the plot

    def update_plot(frame_number, ax):
        ax.clear()
        ax.set_facecolor('black')  # Set background to black for inversion
        
        # Invert the patch (the area containing the event plot) to black
        ax.patch.set_facecolor('black')
        
        # Explicitly set the eventplot colors
        leftsniffing, rightsniffing = events[0]  # Assuming single dataset for single plot
        ax.eventplot([leftsniffing, rightsniffing],
                     colors=['lime', 'orange'], lineoffsets=[1, 2], linelengths=0.5, linewidths=10)
        
        # Set axes properties
        ax.set_xlim(max(0, frame_number - 100), frame_number + 50)  # Adjusted the x-axis window
        ax.set_ylim(0.5, 2.5)  # Reset y-axis limits to original values
        ax.set_yticks([1, 2])
        ax.set_yticklabels(['Stimulus Investigation', 'Drinking'], fontsize=12, fontweight='bold', color='white')
        ax.axvline(x=frame_number, color='cyan', linestyle='--', linewidth=1.5)
        ax.text(frame_number, 2.5, f'Frame: {frame_number}', color='cyan', fontsize=10, verticalalignment='bottom')
        ax.set_title(titles[0], fontsize=14, fontweight='bold', color='white')

        # Set the spines (borders) to black
        for spine in ax.spines.values():
            spine.set_edgecolor('black')

        # Set the x and y labels color to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

    # Create figure with 1 plot
    fig, ax = plt.subplots(figsize=(video_width / 100, plot_height / 100))
    
    # Set the entire figure background to black
    fig.patch.set_facecolor('black')

    for frame_number in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Resize video frame to fit within the new dimensions
        frame_resized = cv2.resize(frame, (video_width, video_height))

        # Update the plot for this frame
        update_plot(frame_number, ax)

        # Convert the plot to an image
        fig.canvas.draw()
        plot_image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        plot_image = plot_image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # Resize plot image to fit video width
        plot_image_resized = cv2.resize(plot_image, (video_width, plot_height))

        # Stack video frame and plot image vertically
        combined_frame = np.vstack((frame_resized, plot_image_resized))
        
        # Write the frame to the output video
        out.write(combined_frame)

    # Release video capture and writer
    cap.release()
    out.release()
    plt.close(fig)

# Example usage
csv_files = [
    r'D:\Eventplots\2024_08_26_16_32_23_testing_side2_40405187_labels.csv'
]
titles = [
    'Ground truth'
]
video_file = r'D:\Eventplots\2024_08_26_16_32_23_testing_side2_40405187DLC_resnet50_New_Setup_sideview_1.0Aug28shuffle1_300000_labeled.mp4'
output_file = r'D:\Eventplots\eventplotdrinking.mp4'
live_event_plot(csv_files, titles, video_file, output_file)