#!/bin/bash
echo " 還原 wlan0 為正常 WiFi 模式..."

# 關閉 Mesh 網卡並還原
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up

# 重新啟動 WiFi 控制服務
sudo systemctl restart wpa_supplicant 2>/dev/null
sudo systemctl restart NetworkManager 2>/dev/null

echo " wlan0 已還原為 Managed 模式，系統將自動連線 WiFi（若有設定）"
