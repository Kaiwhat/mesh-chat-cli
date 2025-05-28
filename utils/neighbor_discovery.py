import subprocess, json, re, os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/nodes.json")

def _get_neighbors_from_dc():
    result = {}
    try:
        out = subprocess.check_output(["batctl", "dc"], text=True)
        print("[除錯] batctl dc 輸出:\n", out)
        for line in out.splitlines():
            match = re.search(r"(\d+\.\d+\.\d+\.\d+).*?(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", line)
            if match:
                ip, mac = match.groups()
                result[ip] = mac.lower()
    except Exception as e:
        print(f"[錯誤] 執行 batctl dc 失敗: {e}")
    return result

def _load_names():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def _save_names(names):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(names, f)

def get_named_neighbors():
    ip_mac_map = _get_neighbors_from_dc()
    names = _load_names()
    result = {}
    for ip, mac in ip_mac_map.items():
        name = names.get(ip, names.get(mac, "未知節點"))
        result[ip] = name
    print("[除錯] 鄰居節點：", result)
    return result

def update_node_name(ip, name):
    names = _load_names()
    names[ip] = name
    _save_names(names)
    return True