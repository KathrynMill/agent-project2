#!/bin/bash
# 专业的Git提交脚本 - 支持回滚

set -e  # 遇到错误立即退出

echo "========================================="
echo "🚀 AI语音助手项目 - Git提交工具"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在git仓库中
if [ ! -d .git ]; then
    echo -e "${RED}❌ 错误：当前目录不是Git仓库！${NC}"
    exit 1
fi

# 显示当前状态
echo -e "${YELLOW}📊 当前Git状态：${NC}"
git status --short
echo ""

# 询问用户操作
echo "请选择操作："
echo "1) 提交所有更改"
echo "2) 只添加新文件"
echo "3) 查看详细状态"
echo "4) 取消"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}✅ 准备提交所有更改...${NC}"
        echo ""
        
        # 添加所有更改
        echo "📝 添加所有文件..."
        git add -A
        
        # 显示将要提交的内容
        echo ""
        echo -e "${YELLOW}📋 将要提交的内容：${NC}"
        git status --short
        echo ""
        
        # 确认提交
        read -p "确认提交? (y/n): " confirm
        if [ "$confirm" != "y" ]; then
            echo -e "${RED}❌ 已取消${NC}"
            exit 0
        fi
        
        # 创建提交
        echo ""
        echo "💬 创建提交信息..."
        git commit -m "feat: 完成AI语音助手v2.0 - 集成讯飞ASR和七牛云LLM

✨ 新增功能：
- 集成讯飞WebSocket ASR实时语音识别
- 集成七牛云DeepSeek-V3大模型
- 实现自研Agent系统（意图识别、任务规划、工具调用）
- 完善系统控制器（打开网站、播放音乐等）
- 美观的Web交互界面
- 支持中英文混合识别

🔧 技术改进：
- 采用讯飞官方Demo实现
- 前端WAV音频录制
- 完善的错误处理
- 详细的文档

🗑️ 清理：
- 删除Node.js冗余文件
- 删除旧版本测试文件
- 清理不再使用的脚本

📚 文档：
- 更新README
- 添加使用说明
- 添加配置指南
- 添加更新日志

🎓 满足课程要求：
- ✅ 调用LLM API
- ✅ 调用ASR/TTS API  
- ✅ 不使用第三方Agent框架
- ✅ 完全自研Agent逻辑"
        
        echo ""
        echo -e "${GREEN}✅ 提交成功！${NC}"
        echo ""
        
        # 显示最近的提交
        echo -e "${YELLOW}📝 最近的提交：${NC}"
        git log --oneline -1
        echo ""
        
        # 询问是否推送
        read -p "是否推送到GitHub? (y/n): " push_confirm
        if [ "$push_confirm" = "y" ]; then
            echo ""
            echo "🚀 正在推送到GitHub..."
            
            # 检查远程仓库
            if ! git remote get-url origin &> /dev/null; then
                echo -e "${RED}❌ 错误：未配置远程仓库！${NC}"
                echo "请先配置远程仓库："
                echo "git remote add origin https://github.com/KathrynMill/agent-project2.git"
                exit 1
            fi
            
            # 推送
            git push origin main || git push origin master
            
            echo ""
            echo -e "${GREEN}✅ 推送成功！${NC}"
            echo "🌐 查看：https://github.com/KathrynMill/agent-project2"
        fi
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}📁 只添加新文件...${NC}"
        git add *.py *.md *.html *.sh frontend/ 2>/dev/null || true
        echo ""
        git status --short
        echo ""
        echo -e "${YELLOW}提示：文件已添加到暂存区，使用以下命令提交：${NC}"
        echo "git commit -m \"你的提交信息\""
        ;;
        
    3)
        echo ""
        echo -e "${YELLOW}📊 详细状态：${NC}"
        git status
        ;;
        
    4)
        echo -e "${YELLOW}👋 已取消${NC}"
        exit 0
        ;;
        
    *)
        echo -e "${RED}❌ 无效选项${NC}"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "💡 回滚提示："
echo "如果需要回滚到上一个版本，使用："
echo "  git reset --soft HEAD~1  # 撤销提交，保留更改"
echo "  git reset --hard HEAD~1  # 撤销提交，丢弃更改"
echo "========================================="

