from flask import Flask, Response, request, jsonify
import cv2
from collections import deque
from evsGrabber import camera_controller

app = Flask(__name__)
frame_queue = deque(maxlen=1)

def generate_frames():
    event_frame_gen = camera_controller.get_frame_generator()
    
    def on_cd_frame_cb(ts, cd_frame):
        ret, buffer = cv2.imencode('.jpg', cd_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if ret:
            frame_queue.append(buffer.tobytes())

    event_frame_gen.set_output_callback(on_cd_frame_cb)

    for evs in camera_controller.mv_iterator:
        event_frame_gen.process_events(evs)
        if frame_queue:
            frame = frame_queue.popleft()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_settings', methods=['POST'])
def update_settings():
    content = request.json
    new_bias_diff_on = content.get('bias_diff_on')
    new_bias_diff_off = content.get('bias_diff_off')

    if new_bias_diff_on is not None and new_bias_diff_off is not None:
        camera_controller.update_settings(bias_diff_on=new_bias_diff_on, bias_diff_off=new_bias_diff_off)
        return jsonify(success=True, message="Camera settings updated.")
    else:
        return jsonify(success=False, message="Invalid settings received.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)