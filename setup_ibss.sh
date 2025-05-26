#!/bin/bash

# 網路參數
IFACE=wlan0
SSID="MeshNet"
FREQ=2412             # channel 1 = 2412 MHz
IP_ADDR="10.0.0.$(shuf -i 10-250 -n 1)"  # 隨機選擇一個節點位址
NETMASK=24

echo "🔧 設定 $IFACE 為 IBSS 模式"

# 關閉 NetworkManager 或 dhcpcd 控制
sudo ip link set $IFACE down
sudo iw dev $IFACE set type ibss
sudo ip link set $IFACE up

echo "📡 加入 IBSS 網路 SSID=$SSID 頻道=2412"
sudo iw dev $IFACE ibss join $SSID $FREQ

echo "🎛️ 設定靜態 IP 為 $IP_ADDR/$NETMASK"
sudo ip addr flush dev $IFACE
sudo ip addr add $IP_ADDR/$NETMASK dev $IFACE

echo "⚙️ 啟用 batman-adv"
sudo modprobe batman-adv
sudo ip link set $IFACE down
sudo iw dev $IFACE set type ibss  # 確保仍為 ibss
sudo ip link set $IFACE up

sudo batctl if add $IFACE
sudo ip link set up dev bat0
sudo ip addr add $IP_ADDR/$NETMASK dev bat0

echo "✅ 完成，現在已加入 Mesh 網路，節點 IP: $IP_ADDR"