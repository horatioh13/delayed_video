import cv2
import time
import os
from delayed_video import jpg_deletion, filter_frame

class DelayedVideoCapture:
    def __init__(self, fps=10, delay=5, quality=50, storage_path='frame_storage', 
                 storage_management=False, special_effects=False):
        self.fps = fps
        self.delay = delay
        self.quality = quality
        self.storage_path = storage_path
        self.storage_management = storage_management
        self.special_effects = special_effects
        
        self.current_frame = None
        self.delayed_frame = None
        self.is_running = False
        self.list_of_times = []
        self.start_time = None
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
    
    def start(self):
        """Start capturing video"""
        self.is_running = True
        self.start_time = time.time()
        self.list_of_times = []
        
        cap = cv2.VideoCapture(0)
        wait_time = 1 / self.fps
        last_frame_time = time.time()
        
        while self.is_running:
            ret, frame = cap.read()
            
            if ret:
                current_time = time.time()
                if current_time - last_frame_time >= wait_time:
                    # Store current frame
                    self.current_frame = frame.copy()
                    
                    # Save frame with timestamp
                    pic_taken_time = round(time.time() - self.start_time, 2)
                    self.list_of_times.append(pic_taken_time)
                    filename = os.path.join(self.storage_path, f"time_{pic_taken_time}.jpg")
                    cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
                    
                    last_frame_time = current_time
            
            # Get delayed frame
            current_time = time.time() - self.start_time
            if current_time > self.delay and self.list_of_times:
                target_time = round(current_time - self.delay, 2)
                closest_time = min(self.list_of_times, key=lambda x: abs(x - target_time))
                closest_filename = os.path.join(self.storage_path, f"time_{closest_time}.jpg")
                
                if os.path.exists(closest_filename):
                    delayed_frame = cv2.imread(closest_filename)
                    
                    if self.special_effects:
                        delayed_frame = filter_frame(delayed_frame, self.delay)
                    
                    self.delayed_frame = delayed_frame
                    
                    if self.storage_management:
                        jpg_deletion(self.storage_path, closest_time, self.list_of_times)
        
        cap.release()
    
    def stop(self):
        """Stop capturing video"""
        self.is_running = False
    
    def get_current_frame(self):
        """Get the current frame as JPEG bytes"""
        if self.current_frame is not None:
            ret, buffer = cv2.imencode('.jpg', self.current_frame)
            return buffer.tobytes()
        return None
    
    def get_delayed_frame(self):
        """Get the delayed frame as JPEG bytes"""
        if self.delayed_frame is not None:
            ret, buffer = cv2.imencode('.jpg', self.delayed_frame)
            return buffer.tobytes()
        return None