import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/node_config.json")

def load_nickname():
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return data.get("nickname", "未命名節點")
    except FileNotFoundError:
        return "未命名節點"

def save_nickname(nickname):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"nickname": nickname}, f)
