import curses
from ui.menu import main_menu
from network import messenger
import threading

if __name__ == '__main__':
    # 啟動背景接收執行緒
    listener_thread = threading.Thread(target=messenger.start_listener, daemon=True)
    listener_thread.start()

    curses.wrapper(main_menu)