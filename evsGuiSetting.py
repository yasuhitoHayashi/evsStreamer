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

def generate_schedule(start_time, interval_minutes, duration_hours, file_duration_minutes):
    schedule = []
    end_time = start_time + timedelta(hours=duration_hours)
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
    start_datetime = st.text_input("Enter start datetime (YYYY-MM-DD HH:MM:SS):")
    interval_minutes = st.number_input("Interval between recordings (minutes):", min_value=1, value=30)
    duration_hours = st.number_input("Total duration of recording (hours):", min_value=1, value=2)
    file_duration_minutes = st.number_input("Duration of each recording file (minutes):", min_value=1, value=10)
    
    if st.button("Generate Schedule"):
        if start_datetime:
            start_time = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
            schedule = generate_schedule(start_time, interval_minutes, duration_hours, file_duration_minutes)
            csv_file_path = "recording_schedule.csv"
            write_schedule_to_csv(schedule, csv_file_path)
            st.success("Schedule created successfully!")
            # CSVファイルの内容を表示
            st.write("Scheduled times:")
            st.write(schedule)
        else:
            st.error("Please enter a valid start datetime.")

if __name__ == "__main__":
    main()
