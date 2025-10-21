#!/bin/bash

# Echo Command Git仓库初始化脚本

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

# 检查Git是否已初始化
check_git_init() {
    if [ ! -d ".git" ]; then
        print_info "初始化Git仓库..."
        git init
        print_success "Git仓库已初始化"
    else
        print_info "Git仓库已存在"
    fi
}

# 配置Git用户信息
setup_git_config() {
    print_info "配置Git用户信息..."
    
    # 设置用户名
    if [ -z "$(git config user.name)" ]; then
        read -p "请输入Git用户名: " git_username
        git config user.name "$git_username"
    fi
    
    # 设置邮箱
    if [ -z "$(git config user.email)" ]; then
        read -p "请输入Git邮箱: " git_email
        git config user.email "$git_email"
    fi
    
    print_success "Git用户信息已配置"
}

# 添加远程仓库
setup_remote() {
    local remote_url="https://github.com/KathrynMill/agent-project2.git"
    
    print_info "配置远程仓库: $remote_url"
    
    # 检查是否已有远程仓库
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

# 创建主分支
create_main_branch() {
    print_info "创建主分支..."
    
    # 检查当前分支
    local current_branch=$(git branch --show-current)
    
    if [ "$current_branch" != "main" ]; then
        git branch -M main
        print_success "主分支已设置为 'main'"
    else
        print_info "当前已在主分支 'main'"
    fi
}

# 创建开发分支
create_develop_branch() {
    print_info "创建开发分支..."
    
    if ! git branch | grep -q "develop"; then
        git checkout -b develop
        print_success "开发分支 'develop' 已创建"
    else
        print_info "开发分支 'develop' 已存在"
    fi
    
    # 切换回主分支
    git checkout main
}

# 创建标签
create_initial_tag() {
    print_info "创建初始标签..."
    
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
    
    print_success "初始标签 'v1.0.0' 已创建"
}

# 设置分支保护规则
setup_branch_protection() {
    print_info "设置分支保护规则..."
    
    print_warning "请手动在GitHub上设置分支保护规则："
    echo "1. 访问: https://github.com/KathrynMill/agent-project2/settings/branches"
    echo "2. 为 'main' 分支添加保护规则："
    echo "   - Require pull request reviews before merging"
    echo "   - Require status checks to pass before merging"
    echo "   - Require branches to be up to date before merging"
    echo "   - Restrict pushes that create files"
    echo "3. 为 'develop' 分支设置类似规则"
}

# 推送到远程仓库
push_to_remote() {
    print_info "推送代码到远程仓库..."
    
    # 推送主分支
    git push -u origin main
    
    # 推送开发分支
    git push -u origin develop
    
    # 推送标签
    git push origin --tags
    
    print_success "代码已推送到远程仓库"
}

# 显示仓库信息
show_repository_info() {
    print_info "仓库信息："
    echo "  远程仓库: $(git remote get-url origin)"
    echo "  主分支: main"
    echo "  开发分支: develop"
    echo "  当前版本: v1.0.0"
    echo "  最新提交: $(git log --oneline -1)"
    
    echo ""
    print_info "GitHub仓库地址："
    echo "  https://github.com/KathrynMill/agent-project2"
    
    echo ""
    print_info "下一步操作："
    echo "1. 设置分支保护规则"
    echo "2. 配置GitHub Actions"
    echo "3. 邀请团队成员"
    echo "4. 开始协作开发"
}

# 主函数
main() {
    print_info "开始设置Git仓库..."
    
    # 1. 初始化Git仓库
    check_git_init
    
    # 2. 配置Git用户信息
    setup_git_config
    
    # 3. 添加远程仓库
    setup_remote
    
    # 4. 创建初始提交
    create_initial_commit
    
    # 5. 创建主分支
    create_main_branch
    
    # 6. 创建开发分支
    create_develop_branch
    
    # 7. 创建初始标签
    create_initial_tag
    
    # 8. 推送到远程仓库
    push_to_remote
    
    # 9. 显示仓库信息
    show_repository_info
    
    # 10. 设置分支保护规则提示
    setup_branch_protection
    
    print_success "🎉 Git仓库设置完成！"
}

main "$@"
