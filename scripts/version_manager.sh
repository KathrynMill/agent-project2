#!/bin/bash

# Echo Command - 版本管理脚本
# 用于创建版本标签、发布和回滚

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION_FILE="$PROJECT_ROOT/VERSION"
CHANGELOG_FILE="$PROJECT_ROOT/CHANGELOG.md"

# 显示帮助信息
show_help() {
    echo -e "${BLUE}Echo Command - 版本管理工具${NC}"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  create <version>    创建新版本标签"
    echo "  release <version>   发布版本到GitHub"
    echo "  rollback <version>  回滚到指定版本"
    echo "  list               列出所有版本"
    echo "  current            显示当前版本"
    echo "  bump <type>        自动升级版本号 (major|minor|patch)"
    echo ""
    echo "选项:"
    echo "  -h, --help         显示此帮助信息"
    echo "  -f, --force        强制操作（跳过确认）"
    echo ""
    echo "示例:"
    echo "  $0 create 1.1.0"
    echo "  $0 release 1.1.0"
    echo "  $0 rollback 1.0.0"
    echo "  $0 bump minor"
}

# 获取当前版本
get_current_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "0.0.0"
    fi
}

# 更新版本文件
update_version_file() {
    local version="$1"
    echo "$version" > "$VERSION_FILE"
    echo -e "${GREEN}✓ 版本文件已更新为: $version${NC}"
}

# 验证版本号格式
validate_version() {
    local version="$1"
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${RED}错误: 版本号格式不正确，应为 x.y.z (如 1.0.0)${NC}"
        exit 1
    fi
}

# 检查Git状态
check_git_status() {
    if [ ! -d ".git" ]; then
        echo -e "${RED}错误: 当前目录不是Git仓库${NC}"
        exit 1
    fi
    
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}警告: 工作目录有未提交的更改${NC}"
        git status --short
        if [ "$FORCE" != "true" ]; then
            read -p "是否继续？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    fi
}

# 创建版本标签
create_version() {
    local version="$1"
    
    echo -e "${BLUE}创建版本 $version...${NC}"
    
    # 检查标签是否已存在
    if git tag -l | grep -q "^v$version$"; then
        echo -e "${YELLOW}警告: 版本标签 v$version 已存在${NC}"
        if [ "$FORCE" != "true" ]; then
            read -p "是否覆盖？(y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
        git tag -d "v$version" 2>/dev/null || true
    fi
    
    # 更新版本文件
    update_version_file "$version"
    
    # 提交版本文件
    git add "$VERSION_FILE"
    git commit -m "chore: bump version to $version" || true
    
    # 创建标签
    git tag -a "v$version" -m "Release version $version"
    
    echo -e "${GREEN}✓ 版本标签 v$version 创建成功${NC}"
}

# 发布版本
release_version() {
    local version="$1"
    
    echo -e "${BLUE}发布版本 $version...${NC}"
    
    # 检查标签是否存在
    if ! git tag -l | grep -q "^v$version$"; then
        echo -e "${RED}错误: 版本标签 v$version 不存在${NC}"
        echo "请先运行: $0 create $version"
        exit 1
    fi
    
    # 推送到远程仓库
    echo "推送标签到远程仓库..."
    git push origin "v$version"
    
    # 如果存在main分支，也推送代码
    if git branch -r | grep -q "origin/main"; then
        git push origin main
    fi
    
    echo -e "${GREEN}✓ 版本 $version 发布成功${NC}"
    echo -e "${BLUE}GitHub链接: https://github.com/KathrynMill/agent-project2/releases/tag/v$version${NC}"
}

# 回滚到指定版本
rollback_version() {
    local version="$1"
    
    echo -e "${BLUE}回滚到版本 $version...${NC}"
    
    # 检查标签是否存在
    if ! git tag -l | grep -q "^v$version$"; then
        echo -e "${RED}错误: 版本标签 v$version 不存在${NC}"
        echo "可用版本:"
        git tag -l | sort -V
        exit 1
    fi
    
    if [ "$FORCE" != "true" ]; then
        echo -e "${YELLOW}警告: 这将重置当前工作目录到版本 $version${NC}"
        read -p "确认继续？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # 硬重置到指定版本
    git reset --hard "v$version"
    
    # 更新版本文件
    update_version_file "$version"
    
    echo -e "${GREEN}✓ 已回滚到版本 $version${NC}"
}

# 列出所有版本
list_versions() {
    echo -e "${BLUE}所有版本标签:${NC}"
    git tag -l | sort -V
    echo ""
    echo -e "${BLUE}当前版本: $(get_current_version)${NC}"
}

# 显示当前版本
show_current_version() {
    echo -e "${BLUE}当前版本: $(get_current_version)${NC}"
}

# 自动升级版本号
bump_version() {
    local bump_type="$1"
    local current_version=$(get_current_version)
    
    # 解析版本号
    IFS='.' read -r major minor patch <<< "$current_version"
    
    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo -e "${RED}错误: 无效的升级类型。使用 major|minor|patch${NC}"
            exit 1
            ;;
    esac
    
    local new_version="$major.$minor.$patch"
    echo -e "${BLUE}升级版本: $current_version -> $new_version${NC}"
    
    create_version "$new_version"
}

# 主函数
main() {
    cd "$PROJECT_ROOT"
    
    # 解析参数
    FORCE="false"
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -f|--force)
                FORCE="true"
                shift
                ;;
            create)
                if [ -z "$2" ]; then
                    echo -e "${RED}错误: 请提供版本号${NC}"
                    exit 1
                fi
                validate_version "$2"
                check_git_status
                create_version "$2"
                exit 0
                ;;
            release)
                if [ -z "$2" ]; then
                    echo -e "${RED}错误: 请提供版本号${NC}"
                    exit 1
                fi
                validate_version "$2"
                release_version "$2"
                exit 0
                ;;
            rollback)
                if [ -z "$2" ]; then
                    echo -e "${RED}错误: 请提供版本号${NC}"
                    exit 1
                fi
                validate_version "$2"
                rollback_version "$2"
                exit 0
                ;;
            list)
                list_versions
                exit 0
                ;;
            current)
                show_current_version
                exit 0
                ;;
            bump)
                if [ -z "$2" ]; then
                    echo -e "${RED}错误: 请提供升级类型 (major|minor|patch)${NC}"
                    exit 1
                fi
                check_git_status
                bump_version "$2"
                exit 0
                ;;
            *)
                echo -e "${RED}错误: 未知命令 '$1'${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    show_help
}

# 运行主函数
main "$@"
