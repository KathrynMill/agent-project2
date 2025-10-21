#!/bin/bash

# Echo Command 安装脚本

echo "安装 Echo Command 应用..."

# 检查系统要求
echo "检查系统要求..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3 (版本3.9+)"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python版本: $PYTHON_VERSION"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装Node.js (版本16+)"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js版本: $NODE_VERSION"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未找到npm，请先安装npm"
    exit 1
fi

echo "✅ npm版本: $(npm --version)"

# 安装后端依赖
echo "安装后端依赖..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
echo "安装Python依赖包..."
pip install -r requirements.txt

# 创建环境配置文件
if [ ! -f ".env" ]; then
    echo "创建环境配置文件..."
    cp env.example .env
    echo "⚠️  请编辑 backend/.env 文件，添加您的OpenAI API Key"
fi

cd ..

# 安装前端依赖
echo "安装前端依赖..."
cd frontend

# 安装npm依赖
npm install

cd ..

# 创建日志目录
echo "创建日志目录..."
mkdir -p backend/logs

# 设置权限
echo "设置文件权限..."
chmod +x start.sh
chmod +x test_system.py

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "1. 编辑 backend/.env 文件，添加您的OpenAI API Key"
echo "2. 运行 ./start.sh 启动应用"
echo "3. 运行 ./test_system.py 测试系统"
echo ""
echo "配置文件位置："
echo "- 后端配置: backend/.env"
echo "- 前端配置: frontend/package.json"
echo ""
echo "启动命令："
echo "- 启动应用: ./start.sh"
echo "- 测试系统: ./test_system.py"
echo "- 仅启动后端: cd backend && source venv/bin/activate && python main.py"
echo "- 仅启动前端: cd frontend && npm run electron:dev"



