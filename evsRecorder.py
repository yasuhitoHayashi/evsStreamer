import os
from datetime import datetime
from metavision_core.event_io.raw_reader import initiate_device

def get_timestamped_filename():
    # 現在の日時を取得し、ファイル名に適した形式で返す
    return datetime.now().strftime("recording_%Y%m%d_%H%M%S.raw")

def start_recording():
    file_path = os.path.abspath(get_timestamped_filename())
    device = initiate_device("")
    events_stream = device.get_i_events_stream()
    if events_stream is None:
        raise RuntimeError("This camera does not support RAW event recording.")

    events_stream.log_raw_data(file_path)
    try:
        events_stream.start()
        print(f"Recording started: {file_path}")
        print("Press Ctrl+C to stop recording.")

        # Keep draining the RAW stream while I_EventsStream writes it to disk.
        # EventsIterator is intentionally not used here: its time slicing is
        # unnecessary for recording and can fail on short live-camera slices.
        while True:
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

if __name__ == "__main__":
    start_recording()
