#!/bin/bash

# Echo Command 版本管理脚本

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

# 获取下一个版本号
get_next_version() {
    local current_version=$(get_current_version)
    local version_type=$1
    
    if [ -z "$version_type" ]; then
        echo "用法: $0 [patch|minor|major]"
        echo "  patch: 补丁版本 (1.0.0 -> 1.0.1)"
        echo "  minor: 次要版本 (1.0.0 -> 1.1.0)"
        echo "  major: 主要版本 (1.0.0 -> 2.0.0)"
        exit 1
    fi
    
    IFS='.' read -ra VERSION_PARTS <<< "$current_version"
    local major=${VERSION_PARTS[0]}
    local minor=${VERSION_PARTS[1]}
    local patch=${VERSION_PARTS[2]}
    
    case $version_type in
        "patch")
            patch=$((patch + 1))
            ;;
        "minor")
            minor=$((minor + 1))
            patch=0
            ;;
        "major")
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        *)
            echo "错误: 无效的版本类型 '$version_type'"
            echo "支持的类型: patch, minor, major"
            exit 1
            ;;
    esac
    
    echo "$major.$minor.$patch"
}

# 更新版本号
update_version() {
    local new_version=$1
    echo "$new_version" > "$VERSION_FILE"
    echo "版本已更新为: $new_version"
}

# 创建Git标签
create_git_tag() {
    local version=$1
    local tag_name="v$version"
    
    if git tag -l | grep -q "^$tag_name$"; then
        echo "标签 $tag_name 已存在"
        return 1
    fi
    
    git add "$VERSION_FILE"
    git commit -m "Bump version to $version"
    git tag -a "$tag_name" -m "Release version $version"
    
    echo "Git标签 $tag_name 已创建"
}

# 更新CHANGELOG.md
update_changelog() {
    local version=$1
    local date=$(date +%Y-%m-%d)
    
    # 在CHANGELOG.md的开头添加新版本
    sed -i "1i\\
## [$version] - $date\\
\\
### 新增\\
- 待添加新功能\\
\\
### 变更\\
- 待添加变更内容\\
\\
### 修复\\
- 待添加修复内容\\
\\
" "$CHANGELOG.md"
    
    echo "CHANGELOG.md 已更新"
}

# 发布版本
release_version() {
    local version_type=$1
    local new_version=$(get_next_version "$version_type")
    local current_version=$(get_current_version)
    
    echo "当前版本: $current_version"
    echo "新版本: $new_version"
    
    read -p "确认发布版本 $new_version? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "发布已取消"
        exit 0
    fi
    
    # 更新版本号
    update_version "$new_version"
    
    # 更新CHANGELOG
    update_changelog "$new_version"
    
    # 创建Git标签
    create_git_tag "$new_version"
    
    echo "✅ 版本 $new_version 发布成功！"
    echo ""
    echo "下一步操作："
    echo "1. 推送标签到远程仓库: git push origin v$new_version"
    echo "2. 创建GitHub Release"
    echo "3. 部署到生产环境"
}

# 显示版本信息
show_version() {
    local current_version=$(get_current_version)
    local git_commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    local git_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    
    echo "Echo Command 版本信息"
    echo "===================="
    echo "版本号: $current_version"
    echo "Git提交: $git_commit"
    echo "Git分支: $git_branch"
    echo "构建时间: $(date)"
}

# 主函数
main() {
    case "$1" in
        "patch"|"minor"|"major")
            release_version "$1"
            ;;
        "show"|"info")
            show_version
            ;;
        "help"|"-h"|"--help")
            echo "Echo Command 版本管理工具"
            echo ""
            echo "用法: $0 [命令]"
            echo ""
            echo "命令:"
            echo "  patch    发布补丁版本 (1.0.0 -> 1.0.1)"
            echo "  minor    发布次要版本 (1.0.0 -> 1.1.0)"
            echo "  major    发布主要版本 (1.0.0 -> 2.0.0)"
            echo "  show     显示当前版本信息"
            echo "  help     显示帮助信息"
            echo ""
            echo "示例:"
            echo "  $0 patch    # 发布补丁版本"
            echo "  $0 minor    # 发布次要版本"
            echo "  $0 show     # 显示版本信息"
            ;;
        *)
            echo "错误: 未知命令 '$1'"
            echo "使用 '$0 help' 查看帮助信息"
            exit 1
            ;;
    esac
}

main "$@"
