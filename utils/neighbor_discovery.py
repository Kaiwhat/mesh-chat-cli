import subprocess, json, re, os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/nodes.json")

def _get_ip_mac_from_tg():
    result = {}
    try:
        out = subprocess.check_output(["batctl", "tg"], text=True)
        print("[除錯] batctl tg 輸出:\n", out)
        for line in out.splitlines():
            match = re.search(r"(\d+\.\d+\.\d+\.\d+).*?(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", line)
            if match:
                ip, mac = match.groups()
                result[mac.lower()] = ip
    except Exception as e:
        print(f"[錯誤] 執行 batctl tg 失敗: {e}")
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
    tg_map = _get_ip_mac_from_tg()
    names = _load_names()
    result = {}
    for mac, ip in tg_map.items():
        name = names.get(mac, "未知節點")
        result[ip] = name
    print("[除錯] 鄰居節點：", result)
    return result

def update_node_name(ip, name):
    tg_map = _get_ip_mac_from_tg()
    for mac, ip_addr in tg_map.items():
        if ip_addr == ip:
            names = _load_names()
            names[mac] = name
            _save_names(names)
            return True
    return False