import os
from evsGrabber import camera_controller

def stop_recording():
    # 生データの記録がアクティブかどうかを確認して停止
    if camera_controller.device.get_i_events_stream():
        camera_controller.device.get_i_events_stream().stop_log_raw_data()

def start_recording(file_path):
    # デバイスが生データストリームをサポートしているか確認
    if camera_controller.device.get_i_events_stream():
        # 生データの記録を開始
        camera_controller.device.get_i_events_stream().log_raw_data(file_path)

        # イベントを取得するためのイテレータを作成
    mv_iterator = camera_controller.get_frame_generator().mv_iterator
    try:
        for evs in mv_iterator:
            pass
    finally:
        # 記録を停止
        stop_recording()

def stop_recording():
    if camera_controller.device.get_i_events_stream():
        camera_controller.device.get_i_events_stream().stop_log_raw_data()

if __name__ == "__main__":
    # 仮のファイルパスを設定
    file_path = "path_to_your_raw_data_file.raw"
    start_recording(file_path)