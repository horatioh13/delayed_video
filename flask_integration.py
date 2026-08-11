from flask import Response
from video_capture import DelayedVideoCapture
import threading

# Global video capture instance
video_capture = None
video_thread = None

def init_video_capture(fps=10, delay=5, quality=50, storage_path='frame_storage',
                       storage_management=False, special_effects=False):
    """Initialize and start video capture in a separate thread"""
    global video_capture, video_thread
    
    if video_capture is None or not video_capture.is_running:
        video_capture = DelayedVideoCapture(fps, delay, quality, storage_path,
                                           storage_management, special_effects)
        video_thread = threading.Thread(target=video_capture.start)
        video_thread.daemon = True
        video_thread.start()
        return True
    return False

def stop_video_capture():
    """Stop video capture"""
    global video_capture
    if video_capture:
        video_capture.stop()
        return True
    return False

def generate_video_stream(stream_type='current'):
    """Generator function for video streaming"""
    global video_capture
    
    while True:
        if video_capture is None:
            break
            
        if stream_type == 'current':
            frame_bytes = video_capture.get_current_frame()
        else:  # delayed
            frame_bytes = video_capture.get_delayed_frame()
        
        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def get_video_feed_response(stream_type='current'):
    """Get Flask Response object for video streaming"""
    return Response(generate_video_stream(stream_type),
                   mimetype='multipart/x-mixed-replace; boundary=frame')