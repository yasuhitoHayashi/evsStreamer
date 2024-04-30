from flask import Flask, Response, request, jsonify
import cv2
from metavision_core.event_io.raw_reader import initiate_device
from metavision_core.event_io import EventsIterator
from metavision_sdk_core import PeriodicFrameGenerationAlgorithm
from collections import deque

app = Flask(__name__)
frame_queue = deque(maxlen=1)  # Store the latest frame

# カメラ設定の初期値とグローバル変数
camera_settings = {
    "bias_diff_on": 0,
    "bias_diff_off": 0
}

def generate_frames():
    evs_source = initiate_device("")
    delta_t = 1E3
    fps = 10
    bias_diff_on = camera_settings["bias_diff_on"]
    bias_diff_off = camera_settings["bias_diff_off"]
    # カメラ設定を取得して更新
    bias_interface = evs_source.get_i_ll_biases()
    bias_interface.set("bias_diff_on", bias_diff_on)
    bias_interface.set("bias_diff_off",bias_diff_off)

    mv_iterator = EventsIterator.from_device(device=evs_source, delta_t=delta_t)
    height, width = mv_iterator.get_size()

    event_frame_gen = PeriodicFrameGenerationAlgorithm(sensor_width=width, sensor_height=height, fps=fps)

    def on_cd_frame_cb(ts, cd_frame):
        ret, buffer = cv2.imencode('.jpg', cd_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])  # 画質設定を追加
        if ret:
            frame_queue.append(buffer.tobytes())

    event_frame_gen.set_output_callback(on_cd_frame_cb)

    for evs in mv_iterator:
        current_bias_diff_on = int(camera_settings["bias_diff_on"])
        current_bias_diff_off = int(camera_settings["bias_diff_off"])
        if bias_diff_on != current_bias_diff_on or bias_diff_off != current_bias_diff_off:
            bias_diff_on = current_bias_diff_on
            bias_diff_off = current_bias_diff_off
            bias_interface.set("bias_diff_on",bias_diff_on)
            bias_interface.set("bias_diff_off",bias_diff_off)

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
    camera_settings["bias_diff_on"] = content.get('bias_diff_on', camera_settings["bias_diff_on"])
    camera_settings["bias_diff_off"] = content.get('bias_diff_off', camera_settings["bias_diff_off"])

    return jsonify(success=True, message="Camera settings updated.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
