#!/bin/bash

# Echo Command - 设置版本管理别名
# 为常用版本管理命令创建便捷别名

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}Echo Command - 设置版本管理别名${NC}"
echo ""

# 检测Shell类型
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo -e "${YELLOW}警告: 未识别的Shell类型，请手动添加别名${NC}"
    exit 1
fi

# 创建别名配置
create_aliases() {
    cat << 'EOF'

# Echo Command - 版本管理别名
alias vpatch='./scripts/quick_version.sh patch'
alias vminor='./scripts/quick_version.sh minor'
alias vmajor='./scripts/quick_version.sh major'
alias vrelease='./scripts/quick_version.sh release'
alias vstatus='./scripts/quick_version.sh status'
alias vrollback='./scripts/quick_version.sh rollback'

# 完整版本管理命令
alias vcreate='./scripts/version_manager.sh create'
alias vlist='./scripts/version_manager.sh list'
alias vcurrent='./scripts/version_manager.sh current'
alias vrollback-full='./scripts/rollback.sh'

# 项目快捷命令
alias vstart='./start.sh'
alias vtest='./test_system.py'
alias vinstall='./install.sh'

# 显示版本管理帮助
alias vhelp='echo "Echo Command 版本管理命令:" && echo "vpatch    - 升级修订号" && echo "vminor    - 升级次版本号" && echo "vmajor    - 升级主版本号" && echo "vrelease  - 发布当前版本" && echo "vstatus   - 显示项目状态" && echo "vrollback - 回滚到上一个版本" && echo "vhelp     - 显示此帮助"'
EOF
}

# 检查别名是否已存在
check_existing_aliases() {
    if grep -q "Echo Command - 版本管理别名" "$SHELL_CONFIG" 2>/dev/null; then
        echo -e "${YELLOW}检测到已存在的别名配置${NC}"
        read -p "是否覆盖现有配置？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # 删除现有配置
            sed -i '/# Echo Command - 版本管理别名/,/^$/d' "$SHELL_CONFIG"
            echo -e "${GREEN}✓ 已删除现有配置${NC}"
        else
            echo "操作已取消"
            exit 0
        fi
    fi
}

# 添加别名到配置文件
add_aliases() {
    echo -e "${BLUE}添加别名到 $SHELL_CONFIG...${NC}"
    
    # 检查文件是否存在
    if [ ! -f "$SHELL_CONFIG" ]; then
        touch "$SHELL_CONFIG"
    fi
    
    # 添加别名
    create_aliases >> "$SHELL_CONFIG"
    
    echo -e "${GREEN}✓ 别名已添加到 $SHELL_CONFIG${NC}"
}

# 显示使用说明
show_usage() {
    echo ""
    echo -e "${GREEN}✓ 别名设置完成！${NC}"
    echo ""
    echo "请运行以下命令重新加载Shell配置："
    echo -e "${BLUE}source $SHELL_CONFIG${NC}"
    echo ""
    echo "或者重新打开终端窗口。"
    echo ""
    echo "设置完成后，您可以使用以下快捷命令："
    echo ""
    echo "版本管理："
    echo "  vpatch    - 升级修订号 (1.0.0 -> 1.0.1)"
    echo "  vminor    - 升级次版本号 (1.0.0 -> 1.1.0)"
    echo "  vmajor    - 升级主版本号 (1.0.0 -> 2.0.0)"
    echo "  vrelease  - 发布当前版本到GitHub"
    echo "  vstatus   - 显示项目状态"
    echo "  vrollback - 回滚到上一个版本"
    echo ""
    echo "项目管理："
    echo "  vstart    - 启动应用"
    echo "  vtest     - 运行测试"
    echo "  vinstall  - 安装依赖"
    echo ""
    echo "帮助："
    echo "  vhelp     - 显示所有命令"
    echo ""
    echo "示例："
    echo "  vpatch    # 修复bug，升级版本"
    echo "  vminor    # 添加新功能"
    echo "  vrelease  # 发布到GitHub"
}

# 主函数
main() {
    cd "$PROJECT_ROOT"
    
    echo "检测到Shell: $SHELL_NAME"
    echo "配置文件: $SHELL_CONFIG"
    echo ""
    
    # 检查现有别名
    check_existing_aliases
    
    # 添加别名
    add_aliases
    
    # 显示使用说明
    show_usage
}

# 运行主函数
main "$@"
