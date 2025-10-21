#!/bin/bash

# Echo Command - GitHub上传脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Git是否安装
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git未安装，请先安装Git："
        echo "  Ubuntu/Debian: sudo apt install git"
        echo "  macOS: brew install git"
        echo "  Windows: 下载 Git for Windows"
        exit 1
    fi
    print_success "Git已安装"
}

# 检查Git配置
check_git_config() {
    if [ -z "$(git config user.name)" ] || [ -z "$(git config user.email)" ]; then
        print_warning "Git用户信息未配置"
        read -p "请输入您的姓名: " git_name
        read -p "请输入您的邮箱: " git_email
        
        git config --global user.name "$git_name"
        git config --global user.email "$git_email"
        print_success "Git用户信息已配置"
    else
        print_info "Git用户信息: $(git config user.name) <$(git config user.email)>"
    fi
}

# 初始化Git仓库
init_git_repo() {
    print_info "初始化Git仓库..."
    
    if [ ! -d ".git" ]; then
        git init
        print_success "Git仓库已初始化"
    else
        print_info "Git仓库已存在"
    fi
}

# 添加远程仓库
add_remote() {
    local remote_url="https://github.com/KathrynMill/agent-project2.git"
    
    print_info "添加远程仓库: $remote_url"
    
    if git remote get-url origin &> /dev/null; then
        print_info "远程仓库已存在: $(git remote get-url origin)"
        read -p "是否要更新远程仓库URL? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote set-url origin "$remote_url"
            print_success "远程仓库URL已更新"
        fi
    else
        git remote add origin "$remote_url"
        print_success "远程仓库已添加"
    fi
}

# 创建初始提交
create_initial_commit() {
    print_info "创建初始提交..."
    
    # 添加所有文件
    git add .
    
    # 创建提交
    git commit -m "Initial commit: Echo Command v1.0.0

🎉 初始版本发布

### 核心功能
- 🎤 语音识别功能 (Whisper)
- 🧠 智能意图理解 (GPT-4o)
- 🔊 语音合成功能 (TTS)
- 🖥️ 系统控制功能
- 📁 文件操作功能
- 💻 Electron桌面应用
- 🌐 WebSocket实时通信
- ⚙️ 跨平台系统控制
- 📊 会话管理和历史记录
- 🎨 现代化用户界面
- 📚 完整项目文档
- 🐳 Docker容器化部署
- 🚀 一键安装和启动脚本

### 技术栈
- 前端: Electron + Vue.js 3 + Element Plus
- 后端: Python + FastAPI + WebSocket
- 云端: Java + Spring Boot + JPA
- AI: OpenAI GPT-4o + Whisper + TTS
- 数据库: MySQL + Redis
- 容器: Docker + Docker Compose
- 监控: Prometheus + Grafana
- CI/CD: GitHub Actions

### 支持平台
- Windows 10/11
- macOS 10.15+
- Ubuntu 18.04+

### 快速开始
1. 运行 ./install.sh 安装依赖
2. 配置 OpenAI API Key
3. 运行 ./start.sh 启动应用
4. 运行 ./test_system.py 测试系统

### 项目结构
- backend/: Python后端服务
- frontend/: Electron前端应用
- cloud/: Java云端服务
- monitoring/: 监控配置
- scripts/: 部署和版本管理脚本
- docs/: 项目文档

### 开发团队
- 项目负责人: Echo Command Team
- 技术栈: 全栈开发
- 开发周期: 2024年1月
- 版本: v1.0.0"
    
    print_success "初始提交已创建"
}

# 设置主分支并推送
setup_main_branch() {
    print_info "设置主分支并推送..."
    
    # 设置主分支
    git branch -M main
    
    # 推送到远程仓库
    print_info "推送到远程仓库..."
    git push -u origin main
    
    print_success "代码已推送到GitHub"
}

# 创建版本标签
create_version_tag() {
    print_info "创建版本标签 v1.0.0..."
    
    git tag -a "v1.0.0" -m "Release version 1.0.0

🎉 Echo Command 初始版本发布

### 主要特性
- 完整的语音控制功能
- 跨平台系统支持
- 现代化用户界面
- 容器化部署方案
- 完整的文档和测试

### 技术亮点
- 混合架构设计
- AI能力集成
- 实时语音交互
- 微服务架构
- 自动化运维

### 快速开始
1. 安装依赖: ./install.sh
2. 配置环境: 编辑 backend/.env
3. 启动应用: ./start.sh
4. 测试系统: ./test_system.py

### 支持平台
- Windows 10/11
- macOS 10.15+
- Ubuntu 18.04+"
    
    # 推送标签
    git push origin v1.0.0
    
    print_success "版本标签 v1.0.0 已创建并推送"
}

# 创建开发分支
create_develop_branch() {
    print_info "创建开发分支..."
    
    git checkout -b develop
    git push -u origin develop
    
    # 切换回main分支
    git checkout main
    
    print_success "开发分支 develop 已创建"
}

# 显示结果
show_results() {
    print_success "🎉 项目已成功上传到GitHub！"
    echo ""
    print_info "仓库信息："
    echo "  仓库地址: https://github.com/KathrynMill/agent-project2"
    echo "  主分支: main"
    echo "  开发分支: develop"
    echo "  当前版本: v1.0.0"
    echo "  最新提交: $(git log --oneline -1)"
    
    echo ""
    print_info "下一步操作："
    echo "1. 访问 https://github.com/KathrynMill/agent-project2 查看仓库"
    echo "2. 设置分支保护规则"
    echo "3. 邀请团队成员"
    echo "4. 创建GitHub Release"
    echo "5. 开始团队协作开发"
    
    echo ""
    print_info "团队协作命令："
    echo "  克隆仓库: git clone https://github.com/KathrynMill/agent-project2.git"
    echo "  创建功能分支: git checkout -b feature/your-feature-name"
    echo "  查看版本: ./scripts/version.sh show"
    echo "  发布新版本: ./scripts/release.sh patch"
}

# 主函数
main() {
    print_info "开始上传Echo Command项目到GitHub..."
    echo ""
    
    # 1. 检查Git
    check_git
    
    # 2. 检查Git配置
    check_git_config
    
    # 3. 初始化Git仓库
    init_git_repo
    
    # 4. 添加远程仓库
    add_remote
    
    # 5. 创建初始提交
    create_initial_commit
    
    # 6. 设置主分支并推送
    setup_main_branch
    
    # 7. 创建版本标签
    create_version_tag
    
    # 8. 创建开发分支
    create_develop_branch
    
    # 9. 显示结果
    show_results
}

# 运行主函数
main "$@"
