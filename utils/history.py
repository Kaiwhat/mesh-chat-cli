import os, json, datetime

HISTORY_DIR = os.path.join(os.path.dirname(__file__), "../history")
os.makedirs(HISTORY_DIR, exist_ok=True)

def save_chat(target, msg):
    filename = os.path.join(HISTORY_DIR, f"{target}.log")
    with open(filename, "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {msg}\n")

def load_chat(target):
    filename = os.path.join(HISTORY_DIR, f"{target}.log")
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return f.readlines()