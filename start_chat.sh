#!/bin/bash

echo "🚀 開始加入 Mesh 網路並啟動聊天系統..."

SCRIPT_DIR=$(dirname "$(realpath "$0")")

echo "🔧 執行 setup_ibss.sh..."
sudo bash "$SCRIPT_DIR/setup_ibss.sh"

echo "⏳ 等待網路介面穩定..."
sleep 3

echo "💬 啟動聊天介面..."
python3 "$SCRIPT_DIR/main.py"