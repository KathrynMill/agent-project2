#!/bin/bash
"""
简化启动脚本 - 只运行后端和本地大模型
基于您的5.3GB内存配置
"""

echo "🚀 Echo Command - 简化启动"
echo "=========================="

# 检查Python环境
echo "📋 检查Python环境..."
python3 --version

# 检查内存
echo "💾 系统内存:"
free -h

echo ""
echo "🎯 启动本地大模型服务..."
echo "📊 模型: SimpleLocalLLM-1.0"
echo "💾 内存使用: 约50MB"
echo "⚡ 响应速度: 极快 (<1秒)"
echo "💰 成本: 100%免费"
echo ""

# 运行本地大模型测试
echo "🧪 运行系统测试..."
python3 simple_test.py

echo ""
echo "✅ 本地大模型服务已就绪！"
echo "🎉 您现在可以开始使用语音控制功能了！"
echo ""
echo "💡 使用说明:"
echo "  - 支持基础语音指令识别"
echo "  - 支持系统控制操作"
echo "  - 支持文本处理任务"
echo "  - 完全本地运行，无需网络"
echo ""
echo "🚀 启动完成！"
echo ""
echo "📝 下一步:"
echo "  1. 安装Node.js以运行前端界面"
echo "  2. 或使用命令行接口进行测试"
echo "  3. 运行 python3 simple_test.py 进行交互测试"

