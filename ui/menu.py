import curses
from network import messenger
from utils import neighbor_discovery, history, config
from wcwidth import wcswidth

def main_menu(stdscr):
    curses.curs_set(0)
    options = ["群組聊天室", "私人對話", "查看聊天記錄", "離開"]
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
                show_history(stdscr)
            elif current_row == 3:
                break
        stdscr.refresh()

def group_chat(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "[群組聊天室] 預設頻道: general，輸入訊息按 Enter 發送，/back 返回\n")
    row = 2
    max_width = curses.COLS - 2
    while True:
        stdscr.addstr(row, 0, "> ")
        msg = stdscr.getstr().decode()
        if msg == "/back":
            break
        messenger.send_broadcast(msg, channel="general")
        formatted = f"[general] {config.load_nickname()}: {msg}"
        padding = max_width - wcswidth(formatted)
        if padding > 0:
            formatted += ' ' * padding
        stdscr.addstr(row + 1, 0, formatted[:max_width])
        history.save_chat("general", msg)
        row += 2
        if row >= curses.LINES - 2:
            stdscr.clear()
            stdscr.addstr(0, 0, "[群組聊天室] 預設頻道: general，輸入訊息按 Enter 發送，/back 返回\n")
            row = 2

def private_chat(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "[私人對話] 掃描中...\n")

    neighbors = neighbor_discovery.get_named_neighbors()
    if not neighbors:
        stdscr.addstr(1, 0, "未發現任何鄰居節點，請確認網路狀態。"); stdscr.getch(); return

    stdscr.addstr(1, 0, "選擇聊天對象：\n")
    for i, (ip, name) in enumerate(neighbors.items()):
        stdscr.addstr(i+2, 2, f"[{i+1}] {name} ({ip})")

    stdscr.addstr(len(neighbors)+3, 0, "請輸入對象編號：")
    idx = int(stdscr.getstr().decode()) - 1
    if idx < 0 or idx >= len(neighbors): return

    ip = list(neighbors.keys())[idx]
    name = list(neighbors.values())[idx]

    stdscr.addstr(len(neighbors)+4, 0, f"是否為此節點命名？目前名稱: {name} (y/n): ")
    choice = stdscr.getstr().decode().lower()
    if choice == 'y':
        stdscr.addstr(len(neighbors)+5, 0, "輸入新名稱：")
        new_name = stdscr.getstr().decode()
        neighbor_discovery.update_node_name(ip, new_name)
        name = new_name

    stdscr.clear()
    stdscr.addstr(0, 0, f"[與 {name} 的私聊] 輸入訊息，/back 返回\n")
    while True:
        stdscr.addstr(2, 0, "> ")
        msg = stdscr.getstr().decode()
        if msg == "/back":
            break
        messenger.send_private(ip, msg)
        history.save_chat(name, msg)

def show_history(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "[聊天記錄] 輸入對象名稱或 general 查看群聊，/back 返回\n")
    stdscr.addstr(2, 0, "對象名稱: ")
    target = stdscr.getstr().decode()
    if target == "/back":
        return
    lines = history.load_chat(target)
    stdscr.clear()
    stdscr.addstr(0, 0, f"與 {target} 的聊天記錄：\n")
    for i, line in enumerate(lines[-10:]):
        stdscr.addstr(i+2, 0, line)
    stdscr.addstr(13, 0, "按任意鍵返回...")
    stdscr.getch()
