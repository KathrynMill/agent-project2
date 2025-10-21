#!/bin/bash
# GitHub上传脚本

set -e

REPO_NAME="echo-command"
GITHUB_USER="KathrynMill"  # 替换为您的GitHub用户名
REMOTE_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo "🚀 Echo Command - GitHub上传工具"
echo "================================="

# 检查Git状态
check_git_status() {
    if [ ! -d ".git" ]; then
        echo "❌ 当前目录不是Git仓库"
        exit 1
    fi
    
    echo "✅ Git仓库状态正常"
}

# 添加所有文件
add_files() {
    echo "📁 添加文件到Git..."
    git add .
    
    # 显示状态
    echo "📊 Git状态:"
    git status --short
}

# 创建提交
create_commit() {
    local message="$1"
    
    if [ -z "$message" ]; then
        message="feat: 初始版本发布 - 完整的语音控制系统"
    fi
    
    echo "💾 创建提交: $message"
    git commit -m "$message"
}

# 设置远程仓库
setup_remote() {
    echo "🔗 设置远程仓库..."
    
    # 检查是否已有远程仓库
    if git remote | grep -q "origin"; then
        echo "✅ 远程仓库已存在"
        git remote -v
    else
        echo "➕ 添加远程仓库: $REMOTE_URL"
        git remote add origin "$REMOTE_URL"
    fi
}

# 推送到GitHub
push_to_github() {
    local branch="${1:-main}"
    
    echo "📤 推送到GitHub..."
    echo "分支: $branch"
    
    # 设置默认分支
    git branch -M "$branch"
    
    # 推送到远程仓库
    git push -u origin "$branch"
    
    echo "✅ 代码已推送到GitHub"
}

# 创建发布标签
create_release_tag() {
    local version=$(cat VERSION 2>/dev/null || echo "1.0.0")
    local tag_name="v$version"
    
    echo "🏷️  创建发布标签: $tag_name"
    
    # 创建带注释的标签
    git tag -a "$tag_name" -m "Release $tag_name - Echo Command语音控制系统"
    
    # 推送标签
    git push origin "$tag_name"
    
    echo "✅ 标签 $tag_name 已创建并推送"
}

# 显示GitHub链接
show_github_links() {
    echo ""
    echo "🔗 GitHub链接:"
    echo "=============="
    echo "仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo "克隆命令: git clone https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo ""
    echo "📋 下一步操作:"
    echo "1. 访问 https://github.com/$GITHUB_USER/$REPO_NAME"
    echo "2. 检查代码是否正确上传"
    echo "3. 创建Release发布"
    echo "4. 设置GitHub Pages（可选）"
}

# 完整上传流程
full_upload() {
    local commit_message="$1"
    local branch="${2:-main}"
    
    echo "🚀 开始完整上传流程..."
    echo ""
    
    # 1. 检查状态
    check_git_status
    
    # 2. 添加文件
    add_files
    
    # 3. 创建提交
    create_commit "$commit_message"
    
    # 4. 设置远程仓库
    setup_remote
    
    # 5. 推送到GitHub
    push_to_github "$branch"
    
    # 6. 创建发布标签
    create_release_tag
    
    # 7. 显示链接
    show_github_links
    
    echo ""
    echo "🎉 上传完成！"
}

# 主函数
main() {
    case "$1" in
        "upload")
            full_upload "$2" "$3"
            ;;
        "status")
            check_git_status
            git status
            ;;
        "add")
            add_files
            ;;
        "commit")
            create_commit "$2"
            ;;
        "push")
            push_to_github "$2"
            ;;
        "tag")
            create_release_tag
            ;;
        "setup")
            setup_remote
            ;;
        *)
            echo "🎯 Echo Command GitHub上传工具"
            echo "================================"
            echo ""
            echo "用法: $0 <command> [options]"
            echo ""
            echo "命令:"
            echo "  upload [message] [branch]  完整上传流程"
            echo "  status                     检查Git状态"
            echo "  add                        添加文件到Git"
            echo "  commit [message]           创建提交"
            echo "  push [branch]              推送到GitHub"
            echo "  tag                        创建发布标签"
            echo "  setup                      设置远程仓库"
            echo ""
            echo "示例:"
            echo "  $0 upload 'feat: 添加语音识别功能' main"
            echo "  $0 status"
            echo "  $0 commit 'fix: 修复端口冲突问题'"
            echo "  $0 push main"
            echo ""
            echo "💡 推荐使用: $0 upload"
            ;;
    esac
}

main "$@"
