import socket
import threading
import json
from utils import config, neighbor_discovery

PORT = 5000
BUFFER = 1024

def format_message(channel, message):
    nickname = config.load_nickname()
    data = {
        "channel": channel,
        "from": nickname,
        "message": message
    }
    return json.dumps(data)

def parse_message(data):
    try:
        msg = json.loads(data)
        return f"[{msg['channel']}] {msg['from']}: {msg['message']}"
    except:
        return data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))

def start_listener():
    print(f"\n[系統] 已啟動接收器，監聽 UDP 埠 {PORT}\n")
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER)
            parsed = parse_message(data.decode())
            print(f"\n[來自 {addr[0]}] {parsed}")
        except Exception as e:
            print(f"[錯誤] 接收失敗: {e}")

def send_broadcast(message, channel="general"):
    formatted = format_message(channel, message)
    neighbors = neighbor_discovery.get_named_neighbors()
    for ip in neighbors.keys():
        try:
            sock.sendto(formatted.encode(), (ip, PORT))
        except Exception as e:
            print(f" 傳送到 {ip} 失敗：{e}")

def send_private(ip, message):
    formatted = format_message("private", message)
    try:
        sock.sendto(formatted.encode(), (ip, PORT))
    except Exception as e:
        print(f" 傳送到 {ip} 失敗：{e}")