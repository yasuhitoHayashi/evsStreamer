import os
from datetime import datetime
from evsGrabber import camera_controller

def stop_recording():
    # 生データの記録がアクティブかどうかを確認して停止
    if camera_controller.device.get_i_events_stream():
        camera_controller.device.get_i_events_stream().stop_log_raw_data()

def get_timestamped_filename():
    # 現在の日時を取得し、ファイル名に適した形式で返す
    return datetime.now().strftime("recording_%Y%m%d_%H%M%S.raw")

def start_recording():
    file_path = get_timestamped_filename()  # ファイル名に日時を追加
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

if __name__ == "__main__":
    start_recording()