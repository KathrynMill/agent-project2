#!/bin/bash
# 版本管理脚本

set -e

VERSION_FILE="VERSION"
CHANGELOG_FILE="CHANGELOG.md"

# 获取当前版本
get_current_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "0.0.0"
    fi
}

# 更新版本号
update_version() {
    local new_version="$1"
    echo "$new_version" > "$VERSION_FILE"
    echo "✅ 版本已更新为: $new_version"
}

# 显示版本信息
show_version() {
    local current_version=$(get_current_version)
    echo "📦 Echo Command 版本信息"
    echo "=========================="
    echo "当前版本: $current_version"
    echo "版本文件: $VERSION_FILE"
    echo "更新日志: $CHANGELOG_FILE"
}

# 创建Git标签
create_tag() {
    local version="$1"
    local message="$2"
    
    if [ -z "$message" ]; then
        message="Release version $version"
    fi
    
    echo "🏷️  创建Git标签: v$version"
    git tag -a "v$version" -m "$message"
    echo "✅ 标签 v$version 已创建"
}

# 发布新版本
release() {
    local version_type="$1"  # major, minor, patch
    local current_version=$(get_current_version)
    
    # 解析版本号
    IFS='.' read -r major minor patch <<< "$current_version"
    
    case "$version_type" in
        "major")
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        "minor")
            minor=$((minor + 1))
            patch=0
            ;;
        "patch")
            patch=$((patch + 1))
            ;;
        *)
            echo "❌ 无效的版本类型: $version_type"
            echo "用法: $0 release [major|minor|patch]"
            exit 1
            ;;
    esac
    
    local new_version="$major.$minor.$patch"
    
    echo "📈 版本升级: $current_version -> $new_version"
    
    # 更新版本文件
    update_version "$new_version"
    
    # 创建Git标签
    create_tag "$new_version" "Release version $new_version"
    
    echo "🎉 版本 $new_version 发布成功！"
    echo "💡 使用 'git push origin v$new_version' 推送到远程仓库"
}

# 回滚到指定版本
rollback() {
    local target_version="$1"
    
    if [ -z "$target_version" ]; then
        echo "❌ 请指定要回滚的版本号"
        echo "用法: $0 rollback <version>"
        exit 1
    fi
    
    echo "🔄 回滚到版本: $target_version"
    
    # 检查标签是否存在
    if ! git tag -l | grep -q "v$target_version"; then
        echo "❌ 版本标签 v$target_version 不存在"
        echo "可用版本:"
        git tag -l | sort -V
        exit 1
    fi
    
    # 回滚到指定版本
    git checkout "v$target_version"
    update_version "$target_version"
    
    echo "✅ 已回滚到版本 $target_version"
}

# 显示所有版本
list_versions() {
    echo "📋 所有版本:"
    echo "============"
    git tag -l | sort -V
}

# 主函数
main() {
    case "$1" in
        "show")
            show_version
            ;;
        "release")
            release "$2"
            ;;
        "rollback")
            rollback "$2"
            ;;
        "list")
            list_versions
            ;;
        "tag")
            create_tag "$2" "$3"
            ;;
        *)
            echo "🎯 Echo Command 版本管理工具"
            echo "=============================="
            echo ""
            echo "用法: $0 <command> [options]"
            echo ""
            echo "命令:"
            echo "  show                   显示当前版本信息"
            echo "  release <type>         发布新版本 (major|minor|patch)"
            echo "  rollback <version>     回滚到指定版本"
            echo "  list                   列出所有版本"
            echo "  tag <version> [msg]    创建版本标签"
            echo ""
            echo "示例:"
            echo "  $0 show"
            echo "  $0 release patch"
            echo "  $0 rollback 1.0.0"
            echo "  $0 tag 1.0.1 '修复语音识别问题'"
            ;;
    esac
}

main "$@"