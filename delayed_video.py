import cv2
import time
import os

def disp_delayed_video():
    cap = cv2.VideoCapture(0)  # Start video capture

    frame_counter = 0  # Initialize a frame counter
    frame_rate = 5 # Frames per second
    wait_time = 1 / frame_rate  # Time to wait between frames
    video_delay_time = 5  # Time to wait before displaying the saved frame

    number_of_frames_to_buffer = video_delay_time*frame_rate

    last_frame_time = time.time()

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if ret:
            current_time = time.time()
            if current_time - last_frame_time >= wait_time:
                # Display the frame
                cv2.imshow('high quality playback', frame)

                # Save the frame as a JPEG file with reduced quality
                filename = os.path.join('frame_storage', f"frame_{frame_counter}.jpg")
                cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 10])
                frame_counter += 1  # Increment the frame counter

                last_frame_time = current_time  # Update the last frame time

        if os.path.exists(filename):
            # Read the saved JPEG file
            saved_frame = cv2.imread(filename)

            # Display the saved frame in a new window
            cv2.imshow('live jpgs', saved_frame)

        delayed_frame_count = frame_counter - number_of_frames_to_buffer
        if delayed_frame_count < 0:
            delayed_frame_count = 0

        delay_frame_filename = os.path.join('frame_storage', f"frame_{delayed_frame_count}.jpg")

        if os.path.exists(delay_frame_filename):
            saved_delayed_frame = cv2.imread(delay_frame_filename)
            cv2.imshow('delayed jpgs', saved_delayed_frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # rm -rf frame_storage/*

    cap.release()
    cv2.destroyAllWindows()

disp_delayed_video()