#!/bin/bash

# Echo Command 发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
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

# 检查Git状态
check_git_status() {
    print_info "检查Git状态..."
    
    if [ -n "$(git status --porcelain)" ]; then
        print_error "工作目录有未提交的更改，请先提交或暂存"
        git status --short
        exit 1
    fi
    
    if [ -n "$(git diff --cached)" ]; then
        print_error "有已暂存但未提交的更改，请先提交"
        exit 1
    fi
    
    print_success "Git状态检查通过"
}

# 运行测试
run_tests() {
    print_info "运行测试..."
    
    # 运行系统测试
    if [ -f "test_system.py" ]; then
        print_info "运行系统测试..."
        python3 test_system.py
    fi
    
    # 运行性能测试
    if [ -f "performance_test.py" ]; then
        print_info "运行性能测试..."
        python3 performance_test.py
    fi
    
    print_success "所有测试通过"
}

# 构建项目
build_project() {
    print_info "构建项目..."
    
    # 构建后端
    if [ -d "backend" ]; then
        print_info "构建后端服务..."
        cd backend
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
        cd ..
    fi
    
    # 构建前端
    if [ -d "frontend" ]; then
        print_info "构建前端应用..."
        cd frontend
        if [ -f "package.json" ]; then
            npm install
            npm run build
        fi
        cd ..
    fi
    
    # 构建云端服务
    if [ -d "cloud" ]; then
        print_info "构建云端服务..."
        cd cloud
        if [ -f "pom.xml" ]; then
            mvn clean package -DskipTests
        fi
        cd ..
    fi
    
    print_success "项目构建完成"
}

# 创建发布包
create_release_package() {
    local version=$1
    local package_name="echo-command-v$version"
    
    print_info "创建发布包: $package_name"
    
    # 创建临时目录
    local temp_dir=$(mktemp -d)
    local release_dir="$temp_dir/$package_name"
    
    # 复制项目文件
    mkdir -p "$release_dir"
    cp -r . "$release_dir/"
    
    # 清理不需要的文件
    cd "$release_dir"
    rm -rf .git
    rm -rf node_modules
    rm -rf venv
    rm -rf __pycache__
    rm -rf *.pyc
    rm -rf .DS_Store
    rm -rf logs/*
    rm -rf data/*
    
    # 创建压缩包
    cd "$temp_dir"
    tar -czf "$package_name.tar.gz" "$package_name"
    zip -r "$package_name.zip" "$package_name"
    
    # 移动发布包到项目根目录
    mv "$package_name.tar.gz" "$OLDPWD/"
    mv "$package_name.zip" "$OLDPWD/"
    
    # 清理临时目录
    rm -rf "$temp_dir"
    
    print_success "发布包已创建: $package_name.tar.gz, $package_name.zip"
}

# 创建GitHub Release
create_github_release() {
    local version=$1
    local tag_name="v$version"
    
    print_info "创建GitHub Release..."
    
    # 检查是否有gh CLI
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI (gh) 未安装，跳过自动创建Release"
        print_info "请手动在GitHub上创建Release: https://github.com/KathrynMill/agent-project2/releases/new"
        return 0
    fi
    
    # 检查是否已登录
    if ! gh auth status &> /dev/null; then
        print_warning "GitHub CLI 未登录，跳过自动创建Release"
        print_info "请运行 'gh auth login' 登录GitHub"
        return 0
    fi
    
    # 创建Release
    local release_notes="## Echo Command v$version

### 新功能
- 待添加新功能

### 改进
- 待添加改进内容

### 修复
- 待添加修复内容

### 安装说明
1. 下载对应平台的安装包
2. 解压到目标目录
3. 运行 ./install.sh 安装依赖
4. 配置环境变量
5. 运行 ./start.sh 启动应用

### 系统要求
- Python 3.9+
- Node.js 16+
- Docker (可选)
- OpenAI API Key"
    
    gh release create "$tag_name" \
        --title "Echo Command v$version" \
        --notes "$release_notes" \
        --draft
    
    print_success "GitHub Release 已创建 (草稿状态)"
    print_info "请编辑Release内容后发布: https://github.com/KathrynMill/agent-project2/releases"
}

# 推送标签
push_tags() {
    print_info "推送标签到远程仓库..."
    
    git push origin --tags
    
    print_success "标签已推送"
}

# 主函数
main() {
    local version_type=$1
    
    if [ -z "$version_type" ]; then
        print_error "用法: $0 [patch|minor|major]"
        echo "  patch: 补丁版本 (1.0.0 -> 1.0.1)"
        echo "  minor: 次要版本 (1.0.0 -> 1.1.0)"
        echo "  major: 主要版本 (1.0.0 -> 2.0.0)"
        exit 1
    fi
    
    print_info "开始发布流程..."
    
    # 1. 检查Git状态
    check_git_status
    
    # 2. 运行测试
    run_tests
    
    # 3. 构建项目
    build_project
    
    # 4. 更新版本号
    local new_version=$(./scripts/version.sh "$version_type" 2>&1 | grep "新版本:" | cut -d' ' -f2)
    
    # 5. 创建发布包
    create_release_package "$new_version"
    
    # 6. 推送标签
    push_tags
    
    # 7. 创建GitHub Release
    create_github_release "$new_version"
    
    print_success "🎉 发布流程完成！"
    print_info "版本: $new_version"
    print_info "标签: v$new_version"
    print_info "发布包: echo-command-v$new_version.tar.gz"
    print_info "GitHub Release: https://github.com/KathrynMill/agent-project2/releases"
    
    echo ""
    print_info "下一步操作："
    echo "1. 检查GitHub Release内容"
    echo "2. 发布Release"
    echo "3. 部署到生产环境"
    echo "4. 通知团队成员"
}

main "$@"
