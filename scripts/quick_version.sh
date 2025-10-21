#!/bin/bash

# Echo Command - 快速版本管理
# 提供简化的版本管理命令

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 显示帮助
show_help() {
    echo -e "${BLUE}Echo Command - 快速版本管理${NC}"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  patch    升级修订号 (1.0.0 -> 1.0.1)"
    echo "  minor    升级次版本号 (1.0.0 -> 1.1.0)"
    echo "  major    升级主版本号 (1.0.0 -> 2.0.0)"
    echo "  release  发布当前版本到GitHub"
    echo "  status   显示当前状态"
    echo "  rollback 回滚到上一个版本"
    echo ""
    echo "示例:"
    echo "  $0 patch    # 修复bug，升级到1.0.1"
    echo "  $0 minor    # 新功能，升级到1.1.0"
    echo "  $0 major    # 重大更新，升级到2.0.0"
    echo "  $0 release  # 发布当前版本"
}

# 获取当前版本
get_current_version() {
    cat "$PROJECT_ROOT/VERSION" 2>/dev/null || echo "0.0.0"
}

# 升级版本并发布
bump_and_release() {
    local bump_type="$1"
    local current_version=$(get_current_version)
    
    echo -e "${BLUE}当前版本: $current_version${NC}"
    
    # 升级版本
    cd "$PROJECT_ROOT"
    ./scripts/version_manager.sh bump "$bump_type"
    
    # 获取新版本
    local new_version=$(get_current_version)
    echo -e "${GREEN}版本已升级: $current_version -> $new_version${NC}"
    
    # 询问是否发布
    read -p "是否发布到GitHub？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./scripts/version_manager.sh release "$new_version"
        echo -e "${GREEN}✓ 版本 $new_version 已发布${NC}"
    else
        echo -e "${BLUE}版本已创建但未发布，可稍后使用 '$0 release' 发布${NC}"
    fi
}

# 发布当前版本
release_current() {
    local current_version=$(get_current_version)
    echo -e "${BLUE}发布版本: $current_version${NC}"
    
    cd "$PROJECT_ROOT"
    ./scripts/version_manager.sh release "$current_version"
    echo -e "${GREEN}✓ 版本 $current_version 已发布${NC}"
}

# 显示状态
show_status() {
    echo -e "${BLUE}Echo Command - 项目状态${NC}"
    echo ""
    echo "当前版本: $(get_current_version)"
    echo ""
    echo "Git状态:"
    git status --short
    echo ""
    echo "最近标签:"
    git tag -l | tail -5
    echo ""
    echo "最近提交:"
    git log --oneline -5
}

# 回滚到上一个版本
rollback_previous() {
    local current_version=$(get_current_version)
    local previous_version=$(git tag -l | sort -V | grep -B1 "v$current_version" | head -1 | sed 's/v//')
    
    if [ -z "$previous_version" ]; then
        echo "没有找到上一个版本"
        exit 1
    fi
    
    echo -e "${BLUE}回滚到版本: $previous_version${NC}"
    cd "$PROJECT_ROOT"
    ./scripts/rollback.sh --backup "$previous_version"
    echo -e "${GREEN}✓ 已回滚到版本 $previous_version${NC}"
}

# 主函数
main() {
    cd "$PROJECT_ROOT"
    
    case "${1:-help}" in
        patch|minor|major)
            bump_and_release "$1"
            ;;
        release)
            release_current
            ;;
        status)
            show_status
            ;;
        rollback)
            rollback_previous
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
