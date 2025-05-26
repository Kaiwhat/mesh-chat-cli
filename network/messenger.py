import socket
import threading
from utils import config

PORT = 5000
BUFFER = 1024

def start_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    print(f"\n[系統] 已啟動接收器，監聽 {PORT} 埠\n")
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER)
            print(f"\n[來自 {addr[0]}]：{data.decode()}")
        except Exception as e:
            print(f"[錯誤] 接收失敗: {e}")

def send_broadcast(message):
    nickname = config.load_nickname()
    formatted = f"[{nickname}] {message}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(formatted.encode(), ("<broadcast>", PORT))

def send_private(ip, message):
    nickname = config.load_nickname()
    formatted = f"[{nickname}] {message}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(formatted.encode(), (ip, PORT))