import subprocess, json, re, os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/nodes.json")

def _get_bat_neighbors():
    try:
        out = subprocess.check_output(["batctl", "n"], text=True)
        print("[除錯] batctl n 輸出:\n", out)
        return re.findall(r"([0-9a-f:]{17})", out)
    except Exception as e:
        print(f"[錯誤] 無法執行 batctl n: {e}")
        return []

def _get_ip_for_mac():
    ip_map = {}
    try:
        out = subprocess.check_output(["ip", "neigh"], text=True)
        print("[除錯] ip neigh 輸出:\n", out)
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 5:
                ip_map[parts[4]] = parts[0]  # MAC -> IP
    except Exception as e:
        print(f"[錯誤] 無法執行 ip neigh: {e}")
    return ip_map

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
    macs = _get_bat_neighbors()
    ip_map = _get_ip_for_mac()
    names = _load_names()
    result = {}
    for mac in macs:
        if mac in ip_map:
            ip = ip_map[mac]
            name = names.get(mac, "未知節點")
            result[ip] = name
    print("[除錯] 鄰居節點：", result)
    return result

def update_node_name(ip, name):
    ip_map = _get_ip_for_mac()
    for mac, ip_addr in ip_map.items():
        if ip_addr == ip:
            names = _load_names()
            names[mac] = name
            _save_names(names)
            return True
    return False