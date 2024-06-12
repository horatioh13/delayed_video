import cv2
import time
import os
import subprocess

def disp_delayed_video(fps,delay,quality):
    cap = cv2.VideoCapture(0)  # Start video capture

    frame_counter = 0  # Initialize a frame counter
    wait_time = 1 / fps  # Time to wait between frames

    number_of_frames_to_buffer = delay*fps

    last_frame_time = time.time()

    # initialize the filename
    filename = 'frame_storage/frame_0.jpg'

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
                cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
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


    cap.release()
    cv2.destroyAllWindows()

def clear_storage():
    subprocess.run('rm -rf frame_storage/*',shell=True)




# fps interger from 1 to 30 (higher untested)
# buffer delay interger from 1 to 600 (higher untested)
# quality interger from 1-100


disp_delayed_video(1, 2, 1)

clear_storage()


