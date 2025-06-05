import socket
import threading
import json
import subprocess

from utils import config, neighbor_discovery
from wcwidth import wcswidth

PORT = 5000
BUFFER = 1024
message_log = []  
MESHTASTIC_PORT   = "/dev/ttyUSB0"
MESHTASTIC_CH_IDX = "2"   #

def format_message(channel, message):
    nickname = config.load_nickname()
    data = {
        "channel": channel,
        "from": nickname,
        "message": message
    }
    return json.dumps(data)

def parse_message(data, width=80):
    try:
        msg = json.loads(data)
        raw = f"[{msg['channel']}] {msg['from']}: {msg['message']}"
        padding = width - wcswidth(raw)
        if padding > 0:
            return raw + ' ' * padding
        return raw
    except:
        return data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))

def start_listener():
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER)
            msg_raw  = data.decode().strip()
            parsed = parse_message(msg_raw)
            message_log.append(parsed)

            result = subprocess.run(
                ["/home/LSA/meshtastic-env/bin/meshtastic",        
                 "--port",     MESHTASTIC_PORT,
                 "--ch-index", MESHTASTIC_CH_IDX,
                 "--sendtext", msg_raw],     
                capture_output=True, text=True
            )
            if result.returncode != 0:        
                message_log.append(f"[轉送失敗] {result.stderr.strip()}")

        except Exception as e:
            message_log.append(f"[錯誤] 接收失敗: {e}")

def get_log():
    return message_log[-10:]  

def send_broadcast(message, channel="general"):
    formatted = format_message(channel, message)
    neighbors = neighbor_discovery.get_named_neighbors()
    for ip in neighbors.keys():
        try:
            sock.sendto(formatted.encode(), (ip, PORT))
        except Exception as e:
            message_log.append(f" 傳送到 {ip} 失敗：{e}")

def send_private(ip, message):
    formatted = format_message("private", message)
    try:
        sock.sendto(formatted.encode(), (ip, PORT))
    except Exception as e:
        message_log.append(f" 傳送到 {ip} 失敗：{e}")
