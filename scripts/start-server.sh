#!/bin/bash

# AI语音助手服务器启动脚本

echo "============================================"
echo "  🎙️  AI语音助手服务器启动脚本"
echo "============================================"
echo ""

# 切换到项目目录
cd "$(dirname "$0")/.." || exit 1
PROJECT_DIR=$(pwd)

echo "📁 项目目录: $PROJECT_DIR"
echo ""

# 检查端口是否被占用
PORT=8090
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  警告: 端口 $PORT 已被占用"
    echo ""
    read -p "是否停止旧进程并重新启动? (y/n): " choice
    if [ "$choice" = "y" ]; then
        echo "🔄 停止旧进程..."
        pkill -f voice_assistant_server.py
        sleep 2
    else
        echo "❌ 取消启动"
        exit 1
    fi
fi

# 启动服务器
echo "🚀 启动服务器..."
echo ""

python3 -u voice_assistant_server.py 2>&1 &
SERVER_PID=$!

echo "✅ 服务器已启动!"
echo "📊 进程ID: $SERVER_PID"
echo ""
echo "============================================"
echo "  访问地址"
echo "============================================"
echo ""
echo "  http://localhost:$PORT/frontend/index.html"
echo ""
echo "============================================"
echo ""
echo "💡 提示:"
echo "  - 按 Ctrl+C 停止服务器"
echo "  - 查看日志: tail -f /var/log/voice-assistant.log"
echo ""

# 等待Ctrl+C
wait $SERVER_PID

