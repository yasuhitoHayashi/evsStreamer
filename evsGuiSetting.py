import streamlit as st
import requests
import streamlit.components.v1 as components
import os
import csv
from datetime import datetime, timedelta

def save_uploaded_file(uploaded_file, path):
    try:
        with open(os.path.join(path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        return False, str(e)

def clear_seconds(dt):
    """秒以下を切り捨てたdatetimeオブジェクトを返す"""
    return dt.replace(second=0, microsecond=0)

def generate_schedule(start_time, end_time, interval_minutes, file_duration_minutes):
    schedule = []
    current_time = start_time
    while current_time < end_time:
        schedule.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        current_time += timedelta(minutes=interval_minutes)
    return schedule

def write_schedule_to_csv(schedule, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['start_time'])
        for time in schedule:
            writer.writerow([time])

def main():
    st.title("Camera Control")
    st.write("Adjust camera settings")

    video_url = "http://localhost:5000/video_feed"
    html_string = f"<img src='{video_url}'/>"
    components.html(html_string, height=500)

    # 初期設定値
    bias_diff_on = st.number_input('Bias Diff ON', min_value=-10, max_value=100, value=30)
    bias_diff_off = st.number_input('Bias Diff OFF', min_value=-10, max_value=100, value=30)

    if st.button('Update Settings'):
        response = requests.post('http://localhost:5000/update_settings', json={
            'bias_diff_on': bias_diff_on,
            'bias_diff_off': bias_diff_off
        })
        if response.json()['success']:
            st.success("Settings updated successfully!")
        else:
            st.error("Failed to update settings.")

    st.header("Schedule Recording")
    # 現在の日時を基準に、選択可能な最小日時と最大日時を設定
    now = clear_seconds(datetime.now())
    max_date = now + timedelta(days=10)  # 未来30日間を選択範囲として設定

    # 日時スライダーで撮影開始日時を設定
    recording_range = st.slider(
        "Select start and end datetime for recording:",
        now, max_date, (now,max_date),
        format = 'Y-M-d H:m',
        step=timedelta(hours=1))

    start_datetime = st.text_input("Set exact start datetime", recording_range[0].strftime('%Y-%m-%d %H:%M'))
    end_datetime = st.text_input("Set exact end datetime", recording_range[1].strftime('%Y-%m-%d %H:%M'))

    start_datetime = recording_range[0]
    end_datetime = recording_range[1]

    # 撮影間隔を分単位で設定
    interval_minutes = st.number_input("Interval between recordings (minutes):", min_value=1, value=30)
    
    # 各撮影ファイルの長さを分単位で設定
    file_duration_minutes = st.number_input("Duration of each recording file (minutes):", min_value=1, value=10)

    if st.button("Generate Schedule"):
        schedule = generate_schedule(start_datetime, end_datetime, interval_minutes, file_duration_minutes)
        csv_file_path = "recording_schedule.csv"
        write_schedule_to_csv(schedule, csv_file_path)
        st.success("Schedule created successfully!")
        st.write("Scheduled times:")
        st.write(schedule)

if __name__ == "__main__":
    main()
