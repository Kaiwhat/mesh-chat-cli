import socket
import threading

PORT = 5000  # Mesh 聊天用預設埠
BUFFER = 1024

def listen_loop(sock):
    while True:
        data, addr = sock.recvfrom(BUFFER)
        print(f"\n👂 來自 {addr[0]}：{data.decode()}")

def main():
    my_ip = socket.gethostbyname(socket.gethostname())
    print(f" 本機啟動 UDP 聊天，監聽埠口 {PORT}")
    print(f" 輸入格式：<對方IP> <訊息內容>")
    print(f" 範例：10.0.0.12 Hello there\n")

    # 建立 socket 並監聽 bat0 上的 UDP 訊息
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))

    threading.Thread(target=listen_loop, args=(sock,), daemon=True).start()

    while True:
        try:
            line = input(" 輸入: ")
            if not line: continue
            if line.strip().lower() == "/exit":
                print(" 離開聊天")
                break
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                print(" 請使用格式：<IP> <訊息>")
                continue
            ip, msg = parts
            sock.sendto(msg.encode(), (ip, PORT))
        except KeyboardInterrupt:
            print("\n 離開聊天")
            break

if __name__ == "__main__":
    main()
