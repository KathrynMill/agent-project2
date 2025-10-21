#!/bin/bash

# Echo Command 启动脚本

echo "启动 Echo Command 应用..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "错误: 未找到Node.js，请先安装Node.js"
    exit 1
fi

# 检查依赖
echo "检查依赖..."

# 检查后端依赖
if [ ! -d "backend/venv" ]; then
    echo "创建Python虚拟环境..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 检查前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "安装前端依赖..."
    cd frontend
    npm install
    cd ..
fi

# 检查环境配置
if [ ! -f "backend/.env" ]; then
    echo "创建环境配置文件..."
    cp backend/env.example backend/.env
    echo "请编辑 backend/.env 文件，添加您的OpenAI API Key"
    echo "然后重新运行此脚本"
    exit 1
fi

# 启动后端服务
echo "启动后端服务..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 5

# 启动前端服务
echo "启动前端服务..."
cd frontend
npm run electron:dev &
FRONTEND_PID=$!
cd ..

# 等待用户中断
echo "应用已启动！按 Ctrl+C 停止服务"
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT

wait

