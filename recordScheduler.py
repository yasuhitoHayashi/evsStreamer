import csv
import schedule
import time
from datetime import datetime, timedelta
import subprocess

def capture():
    # evsRecorder.pyを実行
    subprocess.run(["python", "evsRecorder.py"], check=True)
    print("Capture started at:", datetime.now())

def schedule_captures(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = datetime.strptime(row['start_time'], '%Y-%m-%d %H:%M:%S')
            if start_time > datetime.now():
                # 未来の時間のみをスケジュール
                schedule.every().day.at(start_time.strftime('%H:%M:%S')).do(capture)
                print("Scheduled capture at:", start_time)

if __name__ == "__main__":
    csv_path = 'RecordingSchedule.csv'
    schedule_captures(csv_path)

    # メインループでスケジューラを実行
    while True:
        schedule.run_pending()
        time.sleep(1)
