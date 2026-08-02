import argparse
import os
import time
from datetime import datetime
from metavision_core.event_io.raw_reader import initiate_device

def get_timestamped_filename():
    # 現在の日時を取得し、ファイル名に適した形式で返す
    return datetime.now().strftime("recording_%Y%m%d_%H%M%S.raw")

def start_recording(duration_minutes=None):
    file_path = os.path.abspath(get_timestamped_filename())
    device = initiate_device("")
    events_stream = device.get_i_events_stream()
    if events_stream is None:
        raise RuntimeError("This camera does not support RAW event recording.")

    events_stream.log_raw_data(file_path)
    try:
        events_stream.start()
        print(f"Recording started: {file_path}")
        if duration_minutes is None:
            print("Press Ctrl+C to stop recording.")
            deadline = None
        else:
            print(f"Recording will stop after {duration_minutes:g} minute(s).")
            deadline = time.monotonic() + duration_minutes * 60

        # RAWデータをファイルへ書き込むため、受信バッファを継続して取得する
        while True:
            if deadline is not None and time.monotonic() >= deadline:
                break
            poll_result = events_stream.poll_buffer()
            if poll_result < 0:
                break
            if poll_result > 0:
                events_stream.get_latest_raw_data()
    except KeyboardInterrupt:
        print("Stopping recording...")
    finally:
        try:
            events_stream.stop_log_raw_data()
        finally:
            events_stream.stop()

    print(f"Recording saved: {file_path}")
    return file_path

def positive_minutes(value):
    minutes = float(value)
    if minutes <= 0:
        raise argparse.ArgumentTypeError("minutes must be greater than 0")
    return minutes

def parse_args():
    parser = argparse.ArgumentParser(description="Record RAW events from the camera.")
    parser.add_argument(
        "-m",
        "--minutes",
        type=positive_minutes,
        help="stop recording automatically after this many minutes",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    start_recording(args.minutes)
