import cv2

def motion_detection(input_video_path, output_video_path):
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)
    
    # Get the width and height of the frames in the video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Get the frames per second (fps) of the input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height), isColor=False)
    
    # Read the first frame
    ret, prev_frame = cap.read()
    
    # Convert the frame to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate the absolute difference between the current frame and the previous frame
        frame_diff = cv2.absdiff(gray, prev_gray)
        
        # Write the frame difference to the output video
        out.write(frame_diff)
        
        # Update the previous frame
        prev_gray = gray
    
    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()
    print(f"Motion detection video saved as {output_video_path}")

# Example usage
input_video_path = r'C:/240904_Progress_Report/Eventplots/2024_08_26_16_24_39_urinpresent_top1_40405188DLC_resnet50_New_Setup_topview_1.0Aug27shuffle1_300000_labeled.mp4'  # Path to your input video file
output_video_path = r'C:/240904_Progress_Report/Eventplots/motiontest.mp4'  # Path to save the output video
motion_detection(input_video_path, output_video_path)