# mesh-chat-cli

> 一套用於 Raspberry Pi 的命令列 Mesh 聊天工具，基於 `batman-adv` 與 IBSS 無線模式，可於無網際網路環境中實現即時多人聊天與私人訊息。

---

## 系統需求

- Raspberry Pi
- Raspberry Pi OS
- Python 3.7+
- Dependency：
  - `wcwidth`（中英文混排字寬處理）
  - `curses`（內建於 Python，處理 CLI 介面）

---

## 安裝方式

### 1. Clone

```bash
git clone https://github.com/your-user/mesh-chat-cli.git
cd mesh-chat-cli
````

### 2. 安裝 Python 套件

```bash
pip3 install --break-system-packages wcwidth
```

---

## 快速啟動

### 1. 設定 IBSS + batman-adv（Mesh 模式）

```bash
sudo ./setup_ibss.sh
```

* 將 wlan0 設為 IBSS 模式並加入指定 SSID
* 啟用 batman-adv 模組
* 指派隨機 IP 給 bat0
* 清除 wlan0 IP 以避免路由衝突

### 2. 啟動聊天程式

```bash
./start_chat.sh --name 小明
```

首次執行會提示輸入節點暱稱，並將聊天介面顯示於終端機。

---

## 功能特色

### 基本功能

* `群組聊天室`（預設頻道 general）
* `私人對話`（選擇鄰居節點進行單獨聊天）
* `查看聊天記錄`（本機 log 記錄）
* `掃描`（掃描並顯示所有活躍節點）

### 額外特性

* 自動解析來自他人訊息，並即時更新畫面
* 支援中英文與 emoji 對齊
* 使用者可命名鄰居節點
* 所有訊息皆透過 UDP 廣播或單播封包實作

---

## 使用畫面（文字示意）

```text
╔══════════════════════════════╗
║       Mesh CLI Chat          ║
╠══════════════════════════════╣
║ ▶ 群組聊天室                  
║   私人對話                    
║   查看聊天記錄                 
║   掃描                        
║   離開                        
╚══════════════════════════════╝
↑↓：選擇功能   Enter：執行
```

在聊天室畫面中，底部會自動顯示最近收到的訊息：

```
> Hello everyone
[general] 小明: Hello Pi B
[general] Pi B: Nice to meet you
```

---

## 專案結構

```
mesh-chat-cli/
├── main.py                       # 主程式：啟動 curses UI 與接收器
├── ping_sweep.sh                 # 依序 ping 10.0.0.0 到 10.0.0.255
├── restore_wifi.sh               # 關閉 Mesh 網卡並還原
├── setup_ibss.sh                 # 設定 IBSS + batman-adv script
├── start_chat.sh                 # 一鍵啟動 script（可帶 --name）
├── ui/
│   └── menu.py                   # curses UI 主選單 + 群組訊息 / 私人訊息介面
├── network/
│   └── messenger.py              # 廣播 / 單播封包傳送與接收模組
├── utils/
│   ├── config.py                 # 暱稱載入與儲存（讀寫 node_config.json）
│   ├── history.py                # 讀取與寫入訊息紀錄
│   └── neighbor_discovery.py     # 取得附近節點 IP 與自定義名稱
├── config/
│   └── node_config.json          # 儲存節點暱稱的 JSON 檔（會自動產生）
├── history/
│   └── general.log, ...
```

---

## 測試與除錯

### 查看 bat0 IP

```bash
ip addr show dev bat0
```

### 測試連線

```bash
ping 10.0.0.X
```

### 確認 Mesh 鄰居

```bash
sudo batctl n
sudo batctl dc
```

---

## 注意事項

* 有些 Rasberry Pi 3 內建的 Wi-Fi 模組無法成功建立 Mesh，需要改用支援 IBSS 的 USB 網卡（如 TP-Link TL-WN722N v1、Alfa AWUS036NHA）
* 每次啟動聊天前必須先執行 `setup_ibss.sh`
* 請勿同時以多個終端開啟 `main.py`，避免 port 衝突
