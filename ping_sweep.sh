#/bin/bash

PREFIX="10.0.0"

#最多同時併發的數量(避免過多連線導致資源耗盡)
MAX JOBS=50
job count=0

# 依序 ping 10.0.0.0 到 10.0.0.255
for i in {0..255}; do
    IP="$PREFIX.$i"

    # 背景執行 ping 任務
    (
        if ping -c 1 -W 1 $IP > /dev/null; then
            echo "$IP is reachable"
        else
            echo "$IP is unreachable"
    ) &
    ((job count++) )

    # 控制最多同時併發的任務數量
    if [[ "$job count" -ge "$MAX JOBS" ]] ; then
        wait
        job count=0
    fi
done

# 等待所有背景任務完成
wait