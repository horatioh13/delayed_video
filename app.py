from flask import Flask, render_template, request, jsonify, Response
from flask_integration import init_video_capture, stop_video_capture, get_video_feed_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/delayed_video/start', methods=['POST'])
def start_delayed_video():
    """Start the delayed video capture"""
    data = request.json or {}
    fps = int(data.get('fps', 10))
    delay = int(data.get('delay', 5))
    quality = int(data.get('quality', 50))
    storage_path = data.get('storage_path', 'frame_storage')
    storage_management = data.get('storage_management', False)
    special_effects = data.get('special_effects', False)
    
    success = init_video_capture(fps, delay, quality, storage_path, 
                                 storage_management, special_effects)
    
    if success:
        return jsonify({'status': 'started'})
    return jsonify({'status': 'already running'})

@app.route('/delayed_video/stop', methods=['POST'])
def stop_delayed_video():
    """Stop the delayed video capture"""
    success = stop_video_capture()
    return jsonify({'status': 'stopped' if success else 'not running'})

@app.route('/delayed_video/feed/<stream_type>')
def delayed_video_feed(stream_type):
    """Stream the video feed (current or delayed)"""
    return get_video_feed_response(stream_type)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)