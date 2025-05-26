import curses
from network import messenger

def main_menu(stdscr):
    curses.curs_set(0)
    options = ["群組聊天室", "私人對話", "離開"]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "Mesh CLI Chat - 方向鍵選擇，Enter 執行")
        for idx, row in enumerate(options):
            mode = curses.A_REVERSE if idx == current_row else curses.A_NORMAL
            stdscr.addstr(idx + 2, 2, row, mode)

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            if current_row == 0:
                group_chat(stdscr)
            elif current_row == 1:
                private_chat(stdscr)
            elif current_row == 2:
                break
        stdscr.refresh()

def group_chat(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "[群組聊天室] 輸入訊息，按 Enter 發送，輸入 /back 返回\n")
    while True:
        stdscr.addstr(2, 0, "> ")
        msg = stdscr.getstr().decode()
        if msg == "/back":
            break
        messenger.send_broadcast(msg)

def private_chat(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "[私人對話] 輸入對方 IP，再輸入訊息。輸入 /back 返回\n")
    stdscr.addstr(2, 0, "對方 IP: ")
    ip = stdscr.getstr().decode()
    while True:
        stdscr.addstr(4, 0, "> ")
        msg = stdscr.getstr().decode()
        if msg == "/back":
            break
        messenger.send_private(ip, msg)