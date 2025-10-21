# Echo Command - 版本管理脚本

本目录包含Echo Command项目的版本管理工具和脚本。

## 脚本说明

### 核心脚本

| 脚本 | 功能 | 用法 |
|------|------|------|
| `version_manager.sh` | 完整版本管理 | `./version_manager.sh create 1.1.0` |
| `rollback.sh` | 版本回滚 | `./rollback.sh 1.0.0` |
| `quick_version.sh` | 快速版本管理 | `./quick_version.sh minor` |
| `setup_aliases.sh` | 设置命令别名 | `./setup_aliases.sh` |

### 快速开始

1. **设置别名（推荐）**
   ```bash
   ./scripts/setup_aliases.sh
   source ~/.bashrc  # 或 ~/.zshrc
   ```

2. **使用快捷命令**
   ```bash
   vpatch    # 升级修订号
   vminor    # 升级次版本号
   vmajor    # 升级主版本号
   vrelease  # 发布版本
   vstatus   # 查看状态
   vrollback # 回滚版本
   ```

## 详细用法

### 版本管理脚本 (`version_manager.sh`)

```bash
# 创建新版本
./scripts/version_manager.sh create 1.1.0

# 发布版本
./scripts/version_manager.sh release 1.1.0

# 自动升级版本号
./scripts/version_manager.sh bump minor

# 列出所有版本
./scripts/version_manager.sh list

# 显示当前版本
./scripts/version_manager.sh current
```

### 回滚脚本 (`rollback.sh`)

```bash
# 回滚到指定版本
./scripts/rollback.sh 1.0.0

# 创建备份后回滚
./scripts/rollback.sh --backup 1.0.0

# 列出所有版本
./scripts/rollback.sh --list

# 强制回滚
./scripts/rollback.sh --force 1.0.0
```

### 快速版本管理 (`quick_version.sh`)

```bash
# 升级版本并询问是否发布
./scripts/quick_version.sh patch   # 1.0.0 -> 1.0.1
./scripts/quick_version.sh minor   # 1.0.0 -> 1.1.0
./scripts/quick_version.sh major   # 1.0.0 -> 2.0.0

# 发布当前版本
./scripts/quick_version.sh release

# 查看项目状态
./scripts/quick_version.sh status

# 回滚到上一个版本
./scripts/quick_version.sh rollback
```

## 版本号规则

遵循[语义化版本控制](https://semver.org/lang/zh-CN/)：

- **主版本号（MAJOR）**：不兼容的API修改
- **次版本号（MINOR）**：向下兼容的功能性新增
- **修订号（PATCH）**：向下兼容的问题修正

### 示例

- `1.0.0` → `1.0.1`：修复bug
- `1.0.0` → `1.1.0`：新增功能
- `1.0.0` → `2.0.0`：重大更新

## 发布流程

### 1. 开发阶段
```bash
git checkout -b feature/new-feature
# ... 开发代码 ...
git add .
git commit -m "feat: add new feature"
```

### 2. 创建版本
```bash
# 方式1：使用快速命令
vminor

# 方式2：使用完整命令
./scripts/version_manager.sh create 1.1.0
```

### 3. 发布版本
```bash
# 方式1：使用快速命令
vrelease

# 方式2：使用完整命令
./scripts/version_manager.sh release 1.1.0
```

### 4. GitHub Actions自动发布
推送版本标签后，GitHub Actions会自动：
- 运行测试
- 构建前端
- 创建GitHub Release
- 上传发布包

## 回滚流程

### 1. 查看可用版本
```bash
vstatus
# 或
./scripts/rollback.sh --list
```

### 2. 执行回滚
```bash
# 方式1：回滚到上一个版本
vrollback

# 方式2：回滚到指定版本
./scripts/rollback.sh 1.0.0

# 方式3：创建备份后回滚
./scripts/rollback.sh --backup 1.0.0
```

## 别名设置

运行别名设置脚本后，可以使用以下快捷命令：

### 版本管理
- `vpatch` - 升级修订号
- `vminor` - 升级次版本号
- `vmajor` - 升级主版本号
- `vrelease` - 发布当前版本
- `vstatus` - 显示项目状态
- `vrollback` - 回滚到上一个版本

### 项目管理
- `vstart` - 启动应用
- `vtest` - 运行测试
- `vinstall` - 安装依赖

### 帮助
- `vhelp` - 显示所有命令

## 文件说明

### 版本文件
- `VERSION` - 存储当前版本号
- `CHANGELOG.md` - 记录版本变更

### Git标签
- 格式：`v1.0.0`
- 用途：标记发布版本
- 管理：通过脚本自动创建和删除

## 最佳实践

### 1. 版本发布前
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG.md已更新
- [ ] 版本号已更新

### 2. 回滚前准备
- [ ] 创建备份分支
- [ ] 确认回滚目标版本
- [ ] 通知团队成员

### 3. 提交信息规范
- `feat:` - 新功能
- `fix:` - 修复bug
- `docs:` - 文档更新
- `style:` - 代码格式
- `refactor:` - 代码重构
- `test:` - 测试相关
- `chore:` - 构建过程

## 故障排除

### 常见问题

1. **版本标签已存在**
   ```bash
   git tag -d v1.0.0
   git push origin --delete v1.0.0
   ```

2. **回滚失败**
   ```bash
   git status
   git reset --hard HEAD
   ```

3. **别名不生效**
   ```bash
   source ~/.bashrc  # 或 ~/.zshrc
   ```

### 获取帮助

```bash
# 查看脚本帮助
./scripts/version_manager.sh --help
./scripts/rollback.sh --help
./scripts/quick_version.sh

# 查看项目状态
vstatus
```

## 联系支持

如有问题，请：
1. 查看本文档
2. 检查GitHub Issues
3. 联系开发团队

---

**注意**：版本管理是项目稳定性的重要保障，请严格按照流程操作。
