# Echo Command - 版本管理指南

## 概述

本文档描述了Echo Command项目的版本管理策略，包括版本号规则、发布流程、回滚机制等。

## 版本号规则

我们使用[语义化版本控制](https://semver.org/lang/zh-CN/)（Semantic Versioning）：

- **主版本号（MAJOR）**：不兼容的API修改
- **次版本号（MINOR）**：向下兼容的功能性新增
- **修订号（PATCH）**：向下兼容的问题修正

### 版本号示例
- `1.0.0` - 初始版本
- `1.0.1` - 修复bug
- `1.1.0` - 新增功能
- `2.0.0` - 重大更新（可能不兼容）

## 版本管理工具

### 1. 版本管理脚本 (`scripts/version_manager.sh`)

```bash
# 创建新版本
./scripts/version_manager.sh create 1.1.0

# 发布版本到GitHub
./scripts/version_manager.sh release 1.1.0

# 自动升级版本号
./scripts/version_manager.sh bump minor

# 列出所有版本
./scripts/version_manager.sh list

# 显示当前版本
./scripts/version_manager.sh current
```

### 2. 回滚脚本 (`scripts/rollback.sh`)

```bash
# 回滚到指定版本
./scripts/rollback.sh 1.0.0

# 创建备份后回滚
./scripts/rollback.sh --backup 1.0.0

# 列出所有可用版本
./scripts/rollback.sh --list

# 强制回滚（跳过确认）
./scripts/rollback.sh --force 1.0.0
```

## 发布流程

### 1. 开发阶段
```bash
# 开发新功能
git checkout -b feature/new-feature
# ... 开发代码 ...
git add .
git commit -m "feat: add new feature"
```

### 2. 创建版本
```bash
# 创建新版本标签
./scripts/version_manager.sh create 1.1.0

# 或者自动升级版本号
./scripts/version_manager.sh bump minor
```

### 3. 发布版本
```bash
# 发布到GitHub
./scripts/version_manager.sh release 1.1.0
```

### 4. GitHub Actions自动发布
当推送版本标签时，GitHub Actions会自动：
- 运行测试
- 构建前端
- 创建GitHub Release
- 上传发布包

## 回滚流程

### 1. 查看可用版本
```bash
./scripts/rollback.sh --list
```

### 2. 创建备份（推荐）
```bash
./scripts/rollback.sh --backup 1.0.0
```

### 3. 执行回滚
```bash
./scripts/rollback.sh 1.0.0
```

### 4. 验证回滚
```bash
# 检查版本
./scripts/version_manager.sh current

# 启动应用测试
./start.sh
```

## Git标签管理

### 查看标签
```bash
# 列出所有标签
git tag -l

# 按版本排序
git tag -l | sort -V

# 查看标签详情
git show v1.0.0
```

### 删除标签
```bash
# 删除本地标签
git tag -d v1.0.0

# 删除远程标签
git push origin --delete v1.0.0
```

## 版本文件

### VERSION文件
存储当前版本号：
```
1.0.0
```

### CHANGELOG.md
记录所有版本变更，格式遵循[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)：

```markdown
## [1.1.0] - 2025-01-22

### 新增
- 新功能A
- 新功能B

### 更改
- 改进功能C

### 修复
- 修复问题D
```

## 最佳实践

### 1. 版本发布前检查
- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG.md已更新
- [ ] 版本号已更新

### 2. 回滚前准备
- [ ] 创建备份分支
- [ ] 确认回滚目标版本
- [ ] 通知团队成员

### 3. 版本命名规范
- 标签格式：`v1.0.0`
- 分支格式：`release/v1.0.0`
- 提交信息：`chore: bump version to 1.0.0`

## 常见问题

### Q: 如何撤销错误的版本发布？
A: 使用回滚脚本：
```bash
./scripts/rollback.sh --backup 1.0.0
```

### Q: 如何查看版本历史？
A: 使用Git命令：
```bash
git log --oneline --decorate
git tag -l | sort -V
```

### Q: 如何比较两个版本？
A: 使用Git diff：
```bash
git diff v1.0.0 v1.1.0
```

### Q: 版本发布失败怎么办？
A: 检查GitHub Actions日志，修复问题后重新发布。

## 自动化流程

### GitHub Actions工作流
- **触发条件**：推送版本标签
- **执行步骤**：
  1. 检出代码
  2. 安装依赖
  3. 运行测试
  4. 构建应用
  5. 创建Release
  6. 上传资源

### 手动触发发布
在GitHub仓库页面：
1. 进入Actions标签
2. 选择"Release"工作流
3. 点击"Run workflow"
4. 输入版本号
5. 点击"Run workflow"

## 联系支持

如有版本管理问题，请：
1. 查看本文档
2. 检查GitHub Issues
3. 联系开发团队

---

**注意**：版本管理是项目稳定性的重要保障，请严格按照流程操作。
