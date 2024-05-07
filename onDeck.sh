#!/bin/bash

# スイッチの状態をチェックする関数
check_switch() {
    # スイッチの状態をチェックするコマンド
    echo "OFF"
}

# Wi-Fi アクセスポイントを設定する関数
setup_wifi_access_point() {
    # Wi-Fiアクセスポイントを設定するコマンド
    echo "Setting up WiFi access point..."
}

# メインのロジック
switch_state=$(check_switch)

if [ "$switch_state" = "ON" ]; then
    echo "Switch is ON. Setting up WiFi and starting streaming..."
    setup_wifi_access_point
    python evsStreamer.py &
    python evsGuiSetting.py &
else
    echo "Switch is OFF. Starting record scheduler..."
    python recordScheduler.py &
fi
