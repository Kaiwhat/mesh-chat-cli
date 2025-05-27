# mesh-chat-cli
```bash=
mesh-chat-cli/
├── main.py                        # 主程式：啟動 curses UI 與接收器
├── start_chat.sh                  # 一鍵啟動 script（可帶 --name）
├── setup_ibss.sh                  # 設定 IBSS + batman-adv script
│
├── ui/
│   └── menu.py                    # curses UI 主選單 + 群組訊息 / 私人訊息介面
│
├── network/
│   └── messenger.py               # 廣播 / 單播封包傳送與接收模組
│
├── utils/
│   └── config.py                  # 暱稱載入與儲存（讀寫 node_config.json）
│
├── config/
│   └── node_config.json           # 儲存節點暱稱的 JSON 檔（會自動產生）
│
└── README.md                      # 專案使用說明

```

| 功能項目               | 說明                             |
| ------------------ | ------------------------------ |
| `main.py`          | 啟動 curses UI，使用者可選群組聊天 / 私人訊息      |
| `setup_ibss.sh`    | 自動加入 IBSS + 設定 batman-adv + IP |
| `start_chat.sh`    | 一鍵啟動 script（可帶 `--name` 設定節點暱稱）     |
| `menu.py`          | 類 Ubuntu Server 風格的選單操作       |
| `messenger.py`     | 使用 UDP 廣播 / 單播，附帶暱稱訊息          |
| `config.py`        | 暱稱設定模組，儲存至 `node_config.json`  |
| `node_config.json` | 暱稱設定檔，下次開啟自動使用                 |

## 使用方式 Usage
```bash=
./start_chat.sh --name 小明
```
下次就會記得你的暱稱，不再要求輸入