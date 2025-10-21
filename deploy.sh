#!/bin/bash

# Echo Command 部署脚本

echo "开始部署 Echo Command 应用..."

# 检查Docker和Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ 未找到Docker，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 未找到Docker Compose，请先安装Docker Compose"
    exit 1
fi

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  未设置OPENAI_API_KEY环境变量"
    echo "请设置: export OPENAI_API_KEY=your_api_key_here"
    read -p "是否继续部署? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p logs
mkdir -p data/mysql
mkdir -p data/redis

# 设置权限
echo "设置文件权限..."
chmod +x *.sh

# 停止现有容器
echo "停止现有容器..."
docker-compose down

# 构建镜像
echo "构建Docker镜像..."
docker-compose build

# 启动服务
echo "启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 30

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 运行健康检查
echo "运行健康检查..."
./test_system.py

echo ""
echo "✅ 部署完成！"
echo ""
echo "服务访问地址："
echo "- 前端应用: http://localhost:3000"
echo "- 本地后端: http://localhost:8000"
echo "- 云端服务: http://localhost:8080"
echo "- API文档: http://localhost:8080/swagger-ui.html"
echo ""
echo "管理命令："
echo "- 查看日志: docker-compose logs -f"
echo "- 停止服务: docker-compose down"
echo "- 重启服务: docker-compose restart"
echo "- 更新服务: docker-compose pull && docker-compose up -d"

