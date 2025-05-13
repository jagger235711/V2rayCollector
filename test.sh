#!/bin/bash
if [ -f "subList.csv" ]; then
MAX_PER_BATCH=10
RESULT_FILE="./results/mixed_base64.txt"
> "$RESULT_FILE"
readarray -t links < subList.csv

for ((i=0; i<${#links[@]}; i+=$MAX_PER_BATCH))
do
    batch=("${links[@]:i:$MAX_PER_BATCH}")
    batch_url=$(IFS='|'; echo "${batch[*]}")
    current_url="http://0.0.0.0:25500/sub?target=mixed&url=$batch_url"

    echo "Processing batch $((i/$MAX_PER_BATCH + 1)) with URL: $current_url"
    temp_response=$(mktemp)

    # 新增详细日志记录
    echo ">>> 发送请求到 $current_url 临时文件: $temp_response"
    if  curl -fs -o "$temp_response" -L "$current_url"; then
    
        status=$?
        case $status in
            0)   echo "请求成功" ;;
            6)   echo "无法解析主机" ;;
            7)   echo "无法连接到主机" ;;
            28)  echo "请求超时" ;;
            56)  echo "接收数据失败" ;;
            *)   echo "未知错误: $status" ;;
        esac

        # echo "请求失败，无法获取完整响应"
        # rm -f "$temp_response"
        # exit 1
    fi

    DELAY=0
    while [ ! -s "$temp_response" ]; do
        echo "响应内容 $temp_response 为空，等待 $DELAY 秒后重试..."
        sleep $DELAY
        DELAY=$((DELAY + 1))
        if [ $DELAY -gt 10 ]; then
            echo "重试次数过多，跳过批次"
            rm -f "$temp_response"
            break
        fi
    done

    # 检查并创建结果目录
    if [ ! -d "$RESULT_DIR" ]; then
        echo "创建结果目录: $RESULT_DIR"
        if ! mkdir -p "$RESULT_DIR"; then
            echo "错误：无法创建结果目录"
            exit 1
        fi
    fi

    cat "$temp_response" >> "$RESULT_FILE"
    rm -f "$temp_response"
    echo "批次成功处理"
done
else
echo "subList.csv not found"
exit 1
fi