import curses
from ui.menu import main_menu
from network import messenger
from utils import config
import threading
import os

if __name__ == '__main__':
    if not os.path.exists("config/node_config.json"):
        name = input("請輸入您的節點暱稱：")
        config.save_nickname(name)
    else:
        print(f"✅ 目前使用暱稱：{config.load_nickname()}")

    listener_thread = threading.Thread(target=messenger.start_listener, daemon=True)
    listener_thread.start()

    curses.wrapper(main_menu)
