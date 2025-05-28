#!/bin/bash

echo "開始加入 Mesh 網路並啟動聊天系統..."

SCRIPT_DIR=$(dirname "$(realpath "$0")")

# 如果指定暱稱，就存入 config
if [[ "$1" == "--name" && -n "$2" ]]; then
  echo "設定節點暱稱為：$2"
  mkdir -p "$SCRIPT_DIR/config"
  echo "{ \"nickname\": \"$2\" }" > "$SCRIPT_DIR/config/node_config.json"
fi

echo "🔧 執行 setup_ibss.sh..."
sudo apt install batctl
sudo bash "$SCRIPT_DIR/setup_ibss.sh"

echo "等待網路介面穩定..."
sleep 3

echo "啟動聊天介面..."
python3 "$SCRIPT_DIR/main.py"
