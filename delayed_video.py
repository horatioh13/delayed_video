import cv2
import time
import os
import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, HORIZONTAL, messagebox
import shutil
from flask import Flask, Response

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


def jpg_deletion(storage_path, current_pic_time, list_of_times):
    # Iterate through the list of times and delete files older than the current picture time
    for pic_time in list_of_times:
        if pic_time < current_pic_time:
            filename = os.path.join(storage_path, f"time_{pic_time}.jpg")
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    print(f"Deleted {filename}")
                except Exception as e:
                    print(f"Failed to delete {filename}. Reason: {e}")

    # Remove the deleted times from the list_of_times
    list_of_times[:] = [pic_time for pic_time in list_of_times if pic_time >= current_pic_time]    


def filter_frame(frame, delay):
    # Get the current date and time
    current_time = time.time()
    
    # Subtract the delay from the current time
    delayed_time = current_time - delay
    
    # Convert the delayed time to a readable format
    delayed_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(delayed_time))
    
    # Set the position for the delayed time text (bottom left corner)
    position_bottom_left = (10, frame.shape[0] - 10)
    
    # Set the position for the exhibit text (bottom right corner)
    text_exhibit = "Delayed Reality - by Horatio Montero Hamkins"
    text_size, _ = cv2.getTextSize(text_exhibit, cv2.FONT_HERSHEY_SIMPLEX, 0.3, 1)
    position_bottom_right = (frame.shape[1] - text_size[0] - 10, frame.shape[0] - 10)
    
    # Choose font, scale, color, and thickness
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (255, 255, 255)  # White color
    thickness = 1
    
    # Put the delayed time text on the frame
    cv2.putText(frame, delayed_time_str, position_bottom_left, font, font_scale, color, thickness, cv2.LINE_AA)
    
    # Put the exhibit text on the frame with a smaller font size
    cv2.putText(frame, text_exhibit, position_bottom_right, font, 0.3, color, thickness, cv2.LINE_AA)
    
    # Apply special effects directly
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for example
    
    return frame



def disp_delayed_video2(fps, delay, quality, storage_path, storage_management, special_effects):
    print(f'storage_management: {storage_management}')
    print(f'special_effects: {special_effects}')

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
            if list_of_times:
                closest_time = min(list_of_times, key=lambda x: abs(x - target_time))
                # Construct the filename using the closest time
                closest_filename = os.path.join(storage_path, f"time_{closest_time}.jpg")

                # Check if the file exists and display it
                if os.path.exists(closest_filename):
                    saved_delayed_frame = cv2.imread(closest_filename)

                    if special_effects:
                        saved_delayed_frame = filter_frame(saved_delayed_frame,delay)
                        cv2.namedWindow('closest delayed frame', cv2.WND_PROP_FULLSCREEN)
                        cv2.setWindowProperty('closest delayed frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        cv2.imshow('closest delayed frame', saved_delayed_frame)

                    cv2.imshow('closest delayed frame', saved_delayed_frame)

                    if storage_management:
                        jpg_deletion(storage_path, closest_time, list_of_times)

                else:
                    print("No delay frame file found close to the target time.")
            else:
                print("No frames taken yet.")
            
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def clear_folder(storage_path):
    # Add validation to prevent deleting current directory
    if not storage_path or storage_path.strip() == "":
        print("Error: No storage path specified")
        messagebox.showerror("Error", "Please select a storage path first")
        return
    
    if not os.path.isdir(storage_path):
        print(f"Error: {storage_path} is not a valid directory")
        messagebox.showerror("Error", "Invalid storage path")
        return
    
    # Additional safety check - don't delete current working directory
    if os.path.abspath(storage_path) == os.path.abspath(os.getcwd()):
        messagebox.showerror("Error", "Cannot clear current working directory")
        return
    
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

def start_video_capture_ui(fps, delay, quality, storage_path_label, storage_management, special_effects):
    print(f'storage management state = {storage_management}')
    print(f'special effects state = {special_effects}')
    
    total_delay = delay[0].get() + delay[1].get() * 60 + delay[2].get() * 3600
    storage_path = storage_path_label.cget("text").replace("Storage Path: ", "")
    
    # If no storage path is selected, create a default 'frame_storage' folder
    if storage_path == "":
        storage_path = os.path.join(os.getcwd(), 'frame_storage')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            print(f"Created default storage folder: {storage_path}")
        storage_path_label.config(text=f"Storage Path: {storage_path}")
    
    disp_delayed_video2(fps.get(), total_delay, quality.get(), storage_path, storage_management, special_effects)

def main_gui():
    # Initialize the main window
    root = tk.Tk()
    root.minsize(600, 300)
    root.title("Video Capture Settings")

    global storage_management_state
    storage_management_state = False

    global special_effects_state
    special_effects_state = False

    button_1_state = tk.BooleanVar()
    button_1_state.set(storage_management_state)
    button_2_state = tk.BooleanVar()
    button_2_state.set(special_effects_state)

    # FPS Slider
    fps_label = Label(root, text="Frames per Second (FPS):")
    fps_label.pack()
    fps_slider = Scale(root, from_=1, to=60, orient=HORIZONTAL)
    fps_slider.pack()

    # Delay Slider
    delay_label = Label(root, text="Delay (Seconds):")
    delay_label.pack()
    delay_slider_seconds = Scale(root, from_=0, to=60, orient=HORIZONTAL)
    delay_slider_seconds.pack()

    # Delay Slider (Minutes)
    delay_label_minutes = Label(root, text="Delay (Minutes):")
    delay_label_minutes.pack()
    delay_slider_minutes = Scale(root, from_=0, to=60, orient=HORIZONTAL)
    delay_slider_minutes.pack()

    # Delay Slider (Hours)
    delay_label_hours = Label(root, text="Delay (Hours):")
    delay_label_hours.pack()
    delay_slider_hours = Scale(root, from_=0, to=24, orient=HORIZONTAL)
    delay_slider_hours.pack()

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
    start_button = Button(root, text="Start Video Capture", command=lambda: start_video_capture_ui(fps_slider, [delay_slider_seconds, delay_slider_minutes, delay_slider_hours], quality_slider, storage_path_label, button_1_state.get(), button_2_state.get()))
    start_button.pack()

    # Clear Data Button
    clear_button = Button(root, text="Clear Data", command=lambda: clear_folder(storage_path_label.cget("text").replace("Storage Path: ", "")))
    clear_button.pack()

    # Advanced Settings Button
    advanced_settings_button = Button(root, text="⚙️", command=lambda: open_advanced_settings())
    advanced_settings_button.place(relx=1.0, rely=0.0, anchor='ne')

    def open_advanced_settings():
        # Create a new window for advanced settings
        advanced_settings_window = tk.Toplevel(root)
        advanced_settings_window.title("Advanced Settings")
        
        # Button 1: Toggle Button 1
        button1 = tk.Checkbutton(advanced_settings_window, text="storage management", variable=button_1_state)
        button1.pack()

        # Button 2: Toggle Button 2
        button2 = tk.Checkbutton(advanced_settings_window, text="special effects", variable=button_2_state)
        button2.pack()

        # Define the function to handle the submission
        def submit_button_state():
            global storage_management_state
            global special_effects_state

            # Access the states of the buttons here and pass them to the main script
            storage_management_state = button_1_state.get()
            special_effects_state = button_2_state.get()

            # Close the advanced settings window
            advanced_settings_window.destroy()

        # Submit Button
        submit_button = tk.Button(advanced_settings_window, text="Submit", command=submit_button_state)
        submit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main_gui()

# on usb2.0 maxfps = 6, on my local ssd maxfps = 30
# Lower delay on live feed WHEN USING LOWER FPS setting
# EVEN IF REAL FPS IS LOWER THAN SETTING, THERE WILL BE A DELAY


## add functionality to wipe time list in real time
# add functionality to wipe jpegs in real time

#disp_delayed_video2(60, 30, 1, path)

#clear_folder(path)
