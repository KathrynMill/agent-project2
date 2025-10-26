#!/bin/bash
# 快速提交脚本

cd /home/aa/echo-command

echo "🚀 AI语音助手 - 快速提交到GitHub"
echo ""

# 添加所有文件
echo "📝 添加所有文件..."
git add -A

# 提交
echo "💬 创建提交..."
git commit -m "feat: AI语音助手v2.0 - 集成讯飞ASR和七牛云LLM

✨ 主要功能：
- 讯飞WebSocket语音识别
- 七牛云DeepSeek-V3大模型
- 自研Agent系统
- 系统控制功能
- Web语音交互界面

🎓 满足课程要求：
- 调用LLM/ASR/TTS API
- 不使用第三方Agent框架
- 完全自研Agent逻辑"

echo ""
echo "✅ 提交成功！"
echo ""

# 推送
echo "🚀 推送到GitHub..."
git push origin main 2>/dev/null || git push origin master

echo ""
echo "✅ 完成！"
echo "🌐 查看：https://github.com/KathrynMill/agent-project2"

