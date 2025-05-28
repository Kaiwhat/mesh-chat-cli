import subprocess, json, re, os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config/nodes.json")

def _get_neighbors_by_ping():
    result = {}
    for i in range(1, 255):
        ip = f"10.0.0.{i}"
        try:
            out = subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], stderr=subprocess.DEVNULL, text=True)
            match = re.search(r"icmp_seq=1.*?ttl=\d+.*?time=.*?ms", out)
            if match:
                result[ip] = "未知節點"
        except subprocess.CalledProcessError:
            continue
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
    ip_map = _get_neighbors_by_ping()
    names = _load_names()
    result = {}
    for ip in ip_map:
        name = names.get(ip, "未知節點")
        result[ip] = name
    print("[除錯] 鄰居節點：", result)
    return result

def update_node_name(ip, name):
    names = _load_names()
    names[ip] = name
    _save_names(names)
    return True