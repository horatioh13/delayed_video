import cv2
import time
import os
import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, HORIZONTAL, messagebox
import shutil



def disp_delayed_video(fps, delay, quality, storage_path):

    start_time = time.time()


    if not os.path.exists(storage_path):
        print('directory does not exist')
        quit()

    cap = cv2.VideoCapture(0)  # Start video capture

    frame_counter = 0  # Initialize a frame counter
    wait_time = 1 / fps  # Time to wait between frames

    #number_of_frames_to_buffer = delay * fps

    last_frame_time = time.time()

    # initialize the filename
    filename = os.path.join(storage_path, 'frame_0.jpg')

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if ret:
            current_time = time.time()
            if current_time - last_frame_time >= wait_time:
                # Display the frame
                cv2.imshow('high quality playback', frame)

                # Save the frame as a JPEG file with reduced quality
                filename = os.path.join(storage_path, f"frame_{frame_counter}.jpg")
                cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                frame_counter += 1  # Increment the frame counter

                last_frame_time = current_time  # Update the last frame time
    
        if os.path.exists(filename):
            # Read the saved JPEG file
            saved_frame = cv2.imread(filename)

            # Display the saved frame in a new window
            cv2.imshow('live jpgs', saved_frame)

        #delayed_frame_count = frame_counter - number_of_frames_to_buffer
        #if delayed_frame_count < 0:
            #delayed_frame_count = 0 

        current_time = time.time() - start_time
        if current_time < delay:
            delayed_frame_count = 0
            last_frame = frame_counter
        else:
            delayed_frame_count = frame_counter-last_frame

        delay_frame_filename = os.path.join(storage_path, f"frame_{delayed_frame_count-1}.jpg")

        if os.path.exists(delay_frame_filename):
            saved_delayed_frame = cv2.imread(delay_frame_filename)
            cv2.imshow('delayed jpgs', saved_delayed_frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def disp_delayed_video2(fps, delay, quality, storage_path):

    list_of_times = []

    start_time = time.time()

    if not os.path.exists(storage_path):
        print('directory does not exist')
        quit()

    cap = cv2.VideoCapture(0)  # Start video capture

    wait_time = 1 / fps  # Time to wait between frames

    #number_of_frames_to_buffer = delay * fps

    last_frame_time = time.time()

    # initialize the filename
    filename = os.path.join(storage_path, 'frame_0.jpg')

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if ret:
            current_time = time.time()
            if current_time - last_frame_time >= wait_time:
                # Display the frame
                cv2.imshow('high quality playback', frame)
                current_time2 = time.time()
                pic_taken_time = round(current_time2 - start_time,2)
                list_of_times.append(pic_taken_time)
                # Save the frame as a JPEG file with reduced quality
                filename = os.path.join(storage_path, f"time_{pic_taken_time}.jpg")
                cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

                last_frame_time = current_time  # Update the last frame time
    
        if os.path.exists(filename):
            # Read the saved JPEG file
            saved_frame = cv2.imread(filename)

            # Display the saved frame in a new window
            cv2.imshow('live jpgs', saved_frame)

        current_time = time.time() - start_time
        
        if current_time > delay:
            target_time = round(current_time-delay,2)
            closest_time = min(list_of_times, key=lambda x: abs(x - target_time))
            # Construct the filename using the closest time
            closest_filename = os.path.join(storage_path, f"time_{closest_time}.jpg")

            # Check if the file exists and display it
            if os.path.exists(closest_filename):
                saved_delayed_frame = cv2.imread(closest_filename)
                cv2.imshow('closest delayed frame', saved_delayed_frame)
            else:
                print("No delay frame file found close to the target time.")

            

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()







def clear_folder(storage_path):
    if os.path.isdir(storage_path):
        for item in os.listdir(storage_path):
            item_path = os.path.join(storage_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f'Failed to delete {item_path}. Reason: {e}')

def select_storage_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    folder_path = filedialog.askdirectory()  # Open the folder selection dialog
    root.destroy()  # Destroy the main tkinter window
    return folder_path

def select_storage_path_ui(label):
    folder_path = filedialog.askdirectory()
    label.config(text=f"Storage Path: {folder_path}")
    return folder_path

def start_video_capture_ui(fps, delay, quality, storage_path_label):
    storage_path = storage_path_label.cget("text").replace("Storage Path: ", "")
    if storage_path == "":
        messagebox.showinfo("Error", "Please select a storage path.")
        return
    disp_delayed_video(fps.get(), delay.get(), quality.get(), storage_path)

def main_gui():
    # Initialize the main window
    root = tk.Tk()
    root.title("Video Capture Settings")

    # FPS Slider
    fps_label = Label(root, text="Frames per Second (FPS):")
    fps_label.pack()
    fps_slider = Scale(root, from_=1, to=60, orient=HORIZONTAL)
    fps_slider.pack()

    # Delay Slider
    delay_label = Label(root, text="Delay (Seconds):")
    delay_label.pack()
    delay_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
    delay_slider.pack()

    # Quality Slider
    quality_label = Label(root, text="Quality (1-100):")
    quality_label.pack()
    quality_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL)
    quality_slider.pack()

    # Storage Path Selection
    storage_path_label = Label(root, text="Storage Path: ")
    storage_path_label.pack()
    storage_path_button = Button(root, text="Select Storage Path", command=lambda: select_storage_path_ui(storage_path_label))
    storage_path_button.pack()

    # Start Button
    start_button = Button(root, text="Start Video Capture", command=lambda: start_video_capture_ui(fps_slider, delay_slider, quality_slider, storage_path_label))
    start_button.pack()

    # Clear Data Button
    clear_button = Button(root, text="Clear Data", command=lambda: clear_folder(storage_path_label.cget("text").replace("Storage Path: ", "")))
    clear_button.pack()

    root.mainloop()

#main_gui()

path = '/media/horatio/USB DISK/usb_storage'

disp_delayed_video2(15, 30, 1, path)

#clear_folder(path)
