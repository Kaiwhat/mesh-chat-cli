### main.py
import curses
from ui.menu import main_menu
from network import messenger
from utils import config, neighbor_discovery
import threading
import os
import sys
import subprocess

def check_permissions():
    try:
        subprocess.check_output(["batctl", "n"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        print("  無法執行 'batctl n'，請確認是否擁有 root 權限或已加入 batman 群組")
        print("  解法：請使用以下指令加入群組並重新啟動：")
        print("  sudo groupadd batman")
        print("  sudo chgrp batman /usr/sbin/batctl && sudo chmod g+xs /usr/sbin/batctl")
        print("  sudo usermod -aG batman $USER")
        print("  reboot")
        return False

if __name__ == '__main__':
    if(not check_permissions()): sys.exit(1)

    if not os.path.exists("config/node_config.json"):
        name = input("請輸入您的節點暱稱：")
        config.save_nickname(name)
    else:
        print(f"✅ 目前使用暱稱：{config.load_nickname()}")

    listener_thread = threading.Thread(target=messenger.start_listener, daemon=True)
    listener_thread.start()

    curses.wrapper(main_menu)
