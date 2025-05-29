#!/bin/bash

# Mesh 網路參數（請視情況調整）
IFACE=wlan0
SSID="lsa-mesh"
FREQ=2412  # channel 1 (2.412GHz)
NETMASK=24
IP_ADDR="10.0.0.$(shuf -i 10-250 -n 1)"  # 隨機選一個節點 IP

echo " 停用系統管理無線網卡..."
sudo systemctl stop NetworkManager 2>/dev/null
sudo killall wpa_supplicant 2>/dev/null

echo " 重設 $IFACE 為 IBSS 模式..."
sudo ip link set $IFACE down
sudo iw dev $IFACE set type ibss
sudo ip link set $IFACE up

echo " 加入 IBSS 網路 SSID=$SSID 頻道=$FREQ"
sudo iw dev $IFACE ibss join "$SSID" $FREQ

echo " 清除 wlan0 上的 IP（避免干擾）"
sudo ip addr flush dev $IFACE
sudo rmmod batman-adv

echo " 啟用 batman-adv..."
sudo modprobe batman-adv

# 清除先前加入的介面（若有）
sudo batctl if del $IFACE 2>/dev/null

echo " 將 $IFACE 加入 bat0"
sudo batctl if add $IFACE

echo " 啟動 bat0 介面..."
sudo ip link set up dev bat0

echo " 指定 bat0 IP 為 $IP_ADDR/$NETMASK"
sudo ip addr add $IP_ADDR/$NETMASK dev bat0

echo " 設定完成！"
echo " Mesh IP 位址（bat0）：$IP_ADDR"