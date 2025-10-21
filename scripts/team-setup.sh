#!/bin/bash

# Echo Command 团队开发环境设置脚本

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

# 检查团队成员权限
check_team_permissions() {
    print_info "检查团队成员权限..."
    
    # 检查GitHub CLI
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI (gh) 未安装，请先安装："
        echo "  macOS: brew install gh"
        echo "  Ubuntu: sudo apt install gh"
        echo "  Windows: winget install GitHub.cli"
        return 1
    fi
    
    # 检查是否已登录
    if ! gh auth status &> /dev/null; then
        print_warning "GitHub CLI 未登录，请先登录："
        echo "  gh auth login"
        return 1
    fi
    
    print_success "GitHub CLI 已配置"
}

# 设置开发环境
setup_development_environment() {
    print_info "设置开发环境..."
    
    # 检查必要的工具
    local missing_tools=()
    
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    if ! command -v node &> /dev/null; then
        missing_tools+=("node")
    fi
    
    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "缺少必要的开发工具: ${missing_tools[*]}"
        print_info "请安装缺少的工具后重新运行此脚本"
        return 1
    fi
    
    print_success "开发环境检查通过"
}

# 克隆仓库
clone_repository() {
    local repo_url="https://github.com/KathrynMill/agent-project2.git"
    local clone_dir="echo-command-dev"
    
    print_info "克隆仓库到本地..."
    
    if [ -d "$clone_dir" ]; then
        print_warning "目录 $clone_dir 已存在，是否要更新? (y/N)"
        read -p "" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$clone_dir"
            git pull origin main
            print_success "仓库已更新"
        else
            print_info "跳过仓库克隆"
            return 0
        fi
    else
        git clone "$repo_url" "$clone_dir"
        cd "$clone_dir"
        print_success "仓库已克隆到 $clone_dir"
    fi
}

# 设置开发分支
setup_development_branch() {
    local developer_name=$1
    
    if [ -z "$developer_name" ]; then
        read -p "请输入您的开发者名称 (用于分支命名): " developer_name
    fi
    
    local dev_branch="dev/$developer_name"
    
    print_info "设置开发分支: $dev_branch"
    
    # 创建开发分支
    if ! git branch | grep -q "$dev_branch"; then
        git checkout -b "$dev_branch"
        print_success "开发分支 $dev_branch 已创建"
    else
        git checkout "$dev_branch"
        print_info "已切换到开发分支 $dev_branch"
    fi
}

# 安装项目依赖
install_dependencies() {
    print_info "安装项目依赖..."
    
    # 安装后端依赖
    if [ -d "backend" ]; then
        print_info "安装后端依赖..."
        cd backend
        
        # 创建虚拟环境
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        # 激活虚拟环境
        source venv/bin/activate
        
        # 安装依赖
        pip install --upgrade pip
        pip install -r requirements.txt
        
        cd ..
        print_success "后端依赖安装完成"
    fi
    
    # 安装前端依赖
    if [ -d "frontend" ]; then
        print_info "安装前端依赖..."
        cd frontend
        npm install
        cd ..
        print_success "前端依赖安装完成"
    fi
    
    # 安装云端服务依赖
    if [ -d "cloud" ]; then
        print_info "安装云端服务依赖..."
        cd cloud
        if command -v mvn &> /dev/null; then
            mvn clean install -DskipTests
        else
            print_warning "Maven 未安装，跳过云端服务依赖安装"
        fi
        cd ..
    fi
}

# 配置开发环境
configure_development() {
    print_info "配置开发环境..."
    
    # 创建开发配置文件
    if [ -f "backend/env.example" ] && [ ! -f "backend/.env" ]; then
        cp backend/env.example backend/.env
        print_info "已创建后端配置文件 backend/.env"
        print_warning "请编辑 backend/.env 文件，添加您的 OpenAI API Key"
    fi
    
    # 创建日志目录
    mkdir -p logs
    mkdir -p backend/logs
    mkdir -p cloud/logs
    
    print_success "开发环境配置完成"
}

# 运行测试
run_tests() {
    print_info "运行项目测试..."
    
    # 运行系统测试
    if [ -f "test_system.py" ]; then
        print_info "运行系统测试..."
        python3 test_system.py
    fi
    
    print_success "测试完成"
}

# 设置Git钩子
setup_git_hooks() {
    print_info "设置Git钩子..."
    
    # 创建pre-commit钩子
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Echo Command Pre-commit Hook

echo "Running pre-commit checks..."

# 检查Python代码格式
if [ -d "backend" ]; then
    cd backend
    if command -v black &> /dev/null; then
        echo "Running black formatter..."
        black --check .
    fi
    if command -v flake8 &> /dev/null; then
        echo "Running flake8 linter..."
        flake8 .
    fi
    cd ..
fi

# 检查JavaScript代码格式
if [ -d "frontend" ]; then
    cd frontend
    if [ -f "package.json" ]; then
        echo "Running ESLint..."
        npm run lint
    fi
    cd ..
fi

echo "Pre-commit checks passed!"
EOF
    
    chmod +x .git/hooks/pre-commit
    print_success "Git钩子已设置"
}

# 显示开发指南
show_development_guide() {
    print_info "开发指南："
    echo ""
    echo "📋 开发流程："
    echo "1. 创建功能分支: git checkout -b feature/your-feature-name"
    echo "2. 开发功能并提交: git add . && git commit -m 'feat: add new feature'"
    echo "3. 推送分支: git push origin feature/your-feature-name"
    echo "4. 创建Pull Request"
    echo "5. 代码审查通过后合并到develop分支"
    echo ""
    echo "🔧 常用命令："
    echo "  启动后端: cd backend && source venv/bin/activate && python main.py"
    echo "  启动前端: cd frontend && npm run electron:dev"
    echo "  启动云端: cd cloud && mvn spring-boot:run"
    echo "  运行测试: ./test_system.py"
    echo "  性能测试: ./performance_test.py"
    echo ""
    echo "📚 文档："
    echo "  API文档: http://localhost:8080/swagger-ui.html"
    echo "  项目文档: README.md"
    echo "  架构文档: ARCHITECTURE.md"
    echo ""
    echo "🐛 问题反馈："
    echo "  创建Issue: https://github.com/KathrynMill/agent-project2/issues"
    echo "  讨论区: https://github.com/KathrynMill/agent-project2/discussions"
}

# 主函数
main() {
    local developer_name=$1
    
    print_info "设置团队开发环境..."
    
    # 1. 检查权限
    check_team_permissions
    
    # 2. 设置开发环境
    setup_development_environment
    
    # 3. 克隆仓库
    clone_repository
    
    # 4. 设置开发分支
    setup_development_branch "$developer_name"
    
    # 5. 安装依赖
    install_dependencies
    
    # 6. 配置开发环境
    configure_development
    
    # 7. 运行测试
    run_tests
    
    # 8. 设置Git钩子
    setup_git_hooks
    
    # 9. 显示开发指南
    show_development_guide
    
    print_success "🎉 团队开发环境设置完成！"
    print_info "您现在可以开始开发了！"
}

main "$@"
