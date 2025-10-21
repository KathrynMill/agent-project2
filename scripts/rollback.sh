#!/bin/bash

# Echo Command - 回滚脚本
# 用于安全地回滚到指定版本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 显示帮助信息
show_help() {
    echo -e "${BLUE}Echo Command - 回滚工具${NC}"
    echo ""
    echo "用法: $0 [选项] <版本号>"
    echo ""
    echo "选项:"
    echo "  -h, --help         显示此帮助信息"
    echo "  -l, --list         列出所有可用版本"
    echo "  -b, --backup       创建回滚前的备份"
    echo "  -f, --force        强制回滚（跳过确认）"
    echo "  -c, --clean        回滚后清理未跟踪文件"
    echo ""
    echo "示例:"
    echo "  $0 1.0.0          回滚到版本1.0.0"
    echo "  $0 --list         列出所有版本"
    echo "  $0 --backup 1.0.0 创建备份后回滚"
}

# 列出所有版本
list_versions() {
    echo -e "${BLUE}可用版本:${NC}"
    git tag -l | sort -V
    echo ""
    echo -e "${BLUE}当前版本: $(cat VERSION 2>/dev/null || echo '未知')${NC}"
}

# 创建备份
create_backup() {
    local backup_name="backup-$(date +%Y%m%d-%H%M%S)"
    echo -e "${BLUE}创建备份: $backup_name${NC}"
    
    # 创建备份分支
    git branch "backup/$backup_name" || true
    git push origin "backup/$backup_name" || true
    
    echo -e "${GREEN}✓ 备份已创建: backup/$backup_name${NC}"
}

# 验证版本是否存在
validate_version() {
    local version="$1"
    if ! git tag -l | grep -q "^v$version$"; then
        echo -e "${RED}错误: 版本 v$version 不存在${NC}"
        echo ""
        echo "可用版本:"
        git tag -l | sort -V
        exit 1
    fi
}

# 检查工作目录状态
check_working_directory() {
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}警告: 工作目录有未提交的更改${NC}"
        git status --short
        echo ""
        echo "选项:"
        echo "1. 提交更改"
        echo "2. 暂存更改"
        echo "3. 丢弃更改"
        echo "4. 取消回滚"
        echo ""
        read -p "请选择 (1-4): " choice
        
        case $choice in
            1)
                git add .
                git commit -m "chore: commit changes before rollback"
                ;;
            2)
                git stash push -m "backup before rollback"
                ;;
            3)
                git reset --hard HEAD
                git clean -fd
                ;;
            4)
                echo "回滚已取消"
                exit 0
                ;;
            *)
                echo "无效选择，取消回滚"
                exit 1
                ;;
        esac
    fi
}

# 执行回滚
perform_rollback() {
    local version="$1"
    local clean="$2"
    
    echo -e "${BLUE}回滚到版本 v$version...${NC}"
    
    # 硬重置到指定版本
    git reset --hard "v$version"
    
    # 更新版本文件
    echo "$version" > VERSION
    
    # 清理未跟踪文件（如果指定）
    if [ "$clean" = "true" ]; then
        echo -e "${BLUE}清理未跟踪文件...${NC}"
        git clean -fd
    fi
    
    echo -e "${GREEN}✓ 已成功回滚到版本 v$version${NC}"
}

# 显示回滚后信息
show_post_rollback_info() {
    local version="$1"
    echo ""
    echo -e "${BLUE}回滚完成！${NC}"
    echo ""
    echo "当前版本: $version"
    echo "Git状态:"
    git status --short
    echo ""
    echo "下一步操作:"
    echo "1. 测试应用功能"
    echo "2. 如有问题，可以再次回滚"
    echo "3. 确认无误后，可以继续开发"
    echo ""
    echo "常用命令:"
    echo "  git log --oneline -10    # 查看最近提交"
    echo "  git status               # 查看状态"
    echo "  ./start.sh               # 启动应用"
}

# 主函数
main() {
    cd "$PROJECT_ROOT"
    
    # 默认参数
    BACKUP="false"
    FORCE="false"
    CLEAN="false"
    VERSION=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -l|--list)
                list_versions
                exit 0
                ;;
            -b|--backup)
                BACKUP="true"
                shift
                ;;
            -f|--force)
                FORCE="true"
                shift
                ;;
            -c|--clean)
                CLEAN="true"
                shift
                ;;
            -*)
                echo -e "${RED}错误: 未知选项 '$1'${NC}"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$VERSION" ]; then
                    VERSION="$1"
                else
                    echo -e "${RED}错误: 只能指定一个版本号${NC}"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # 检查是否提供了版本号
    if [ -z "$VERSION" ]; then
        echo -e "${RED}错误: 请提供版本号${NC}"
        show_help
        exit 1
    fi
    
    # 验证版本
    validate_version "$VERSION"
    
    # 显示确认信息
    echo -e "${YELLOW}准备回滚到版本 v$VERSION${NC}"
    echo ""
    echo "这将执行以下操作:"
    echo "1. 重置代码到版本 v$VERSION"
    echo "2. 更新版本文件"
    if [ "$CLEAN" = "true" ]; then
        echo "3. 清理未跟踪文件"
    fi
    echo ""
    
    # 创建备份
    if [ "$BACKUP" = "true" ]; then
        create_backup
    fi
    
    # 检查工作目录
    if [ "$FORCE" != "true" ]; then
        check_working_directory
    fi
    
    # 最终确认
    if [ "$FORCE" != "true" ]; then
        read -p "确认回滚？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "回滚已取消"
            exit 0
        fi
    fi
    
    # 执行回滚
    perform_rollback "$VERSION" "$CLEAN"
    
    # 显示回滚后信息
    show_post_rollback_info "$VERSION"
}

# 运行主函数
main "$@"
