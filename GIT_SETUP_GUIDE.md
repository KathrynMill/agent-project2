# Echo Command - Git仓库设置指南

## 🎯 目标
将Echo Command项目上传到GitHub仓库：`https://github.com/KathrynMill/agent-project2`

## 📋 前置要求
1. 安装Git: `sudo apt install git` (Ubuntu) 或 `brew install git` (macOS)
2. 配置Git用户信息
3. 设置SSH密钥或使用HTTPS认证

## 🚀 快速设置

### 1. 安装Git (如果未安装)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git

# macOS
brew install git

# Windows
# 下载并安装 Git for Windows
```

### 2. 配置Git用户信息
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. 设置SSH密钥 (推荐)
```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "your.email@example.com"

# 添加到SSH代理
ssh-add ~/.ssh/id_ed25519

# 复制公钥到剪贴板
cat ~/.ssh/id_ed25519.pub

# 在GitHub上添加SSH密钥
# 访问: https://github.com/settings/keys
```

### 4. 初始化项目仓库
```bash
# 进入项目目录
cd /home/aa/echo-command

# 初始化Git仓库
git init

# 添加远程仓库
git remote add origin https://github.com/KathrynMill/agent-project2.git

# 或者使用SSH (推荐)
git remote add origin git@github.com:KathrynMill/agent-project2.git
```

### 5. 创建初始提交
```bash
# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: Echo Command v1.0.0

🎉 初始版本发布

### 核心功能
- 🎤 语音识别功能 (Whisper)
- 🧠 智能意图理解 (GPT-4o)
- 🔊 语音合成功能 (TTS)
- 🖥️ 系统控制功能
- 📁 文件操作功能
- 💻 Electron桌面应用
- 🌐 WebSocket实时通信
- ⚙️ 跨平台系统控制
- 📊 会话管理和历史记录
- 🎨 现代化用户界面
- 📚 完整项目文档
- 🐳 Docker容器化部署
- 🚀 一键安装和启动脚本

### 技术栈
- 前端: Electron + Vue.js 3 + Element Plus
- 后端: Python + FastAPI + WebSocket
- 云端: Java + Spring Boot + JPA
- AI: OpenAI GPT-4o + Whisper + TTS
- 数据库: MySQL + Redis
- 容器: Docker + Docker Compose
- 监控: Prometheus + Grafana
- CI/CD: GitHub Actions

### 支持平台
- Windows 10/11
- macOS 10.15+
- Ubuntu 18.04+

### 快速开始
1. 运行 ./install.sh 安装依赖
2. 配置 OpenAI API Key
3. 运行 ./start.sh 启动应用
4. 运行 ./test_system.py 测试系统

### 项目结构
- backend/: Python后端服务
- frontend/: Electron前端应用
- cloud/: Java云端服务
- monitoring/: 监控配置
- scripts/: 部署和版本管理脚本
- docs/: 项目文档

### 开发团队
- 项目负责人: Echo Command Team
- 技术栈: 全栈开发
- 开发周期: 2024年1月
- 版本: v1.0.0"

# 创建主分支
git branch -M main

# 推送到远程仓库
git push -u origin main
```

### 6. 创建版本标签
```bash
# 创建v1.0.0标签
git tag -a "v1.0.0" -m "Release version 1.0.0

🎉 Echo Command 初始版本发布

### 主要特性
- 完整的语音控制功能
- 跨平台系统支持
- 现代化用户界面
- 容器化部署方案
- 完整的文档和测试

### 技术亮点
- 混合架构设计
- AI能力集成
- 实时语音交互
- 微服务架构
- 自动化运维

### 快速开始
1. 安装依赖: ./install.sh
2. 配置环境: 编辑 backend/.env
3. 启动应用: ./start.sh
4. 测试系统: ./test_system.py

### 支持平台
- Windows 10/11
- macOS 10.15+
- Ubuntu 18.04+"

# 推送标签
git push origin v1.0.0
```

## 🔧 团队开发设置

### 1. 设置开发分支
```bash
# 创建开发分支
git checkout -b develop
git push -u origin develop

# 创建功能分支
git checkout -b feature/your-feature-name
```

### 2. 设置分支保护规则
访问: https://github.com/KathrynMill/agent-project2/settings/branches

为以下分支设置保护规则：
- `main` 分支：生产环境代码
- `develop` 分支：开发环境代码

保护规则设置：
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Restrict pushes that create files

### 3. 邀请团队成员
访问: https://github.com/KathrynMill/agent-project2/settings/access

添加团队成员并设置权限：
- **Admin**: 完全访问权限
- **Maintain**: 管理仓库权限
- **Write**: 推送权限
- **Triage**: 管理Issues和PR权限
- **Read**: 只读权限

## 📊 版本管理

### 版本号规则
- **主版本号 (Major)**: 不兼容的API修改
- **次版本号 (Minor)**: 向下兼容的功能性新增
- **修订号 (Patch)**: 向下兼容的问题修正

### 发布流程
```bash
# 发布补丁版本 (1.0.0 -> 1.0.1)
./scripts/release.sh patch

# 发布次版本 (1.0.0 -> 1.1.0)
./scripts/release.sh minor

# 发布主版本 (1.0.0 -> 2.0.0)
./scripts/release.sh major
```

### 版本管理命令
```bash
# 查看当前版本
./scripts/version.sh show

# 更新版本号
./scripts/version.sh patch
./scripts/version.sh minor
./scripts/version.sh major
```

## 🔄 开发工作流

### 1. 功能开发流程
```bash
# 1. 从develop分支创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. 开发功能
# ... 编写代码 ...

# 3. 提交代码
git add .
git commit -m "feat: add new feature"

# 4. 推送分支
git push origin feature/new-feature

# 5. 创建Pull Request
# 在GitHub上创建PR，请求合并到develop分支
```

### 2. 问题修复流程
```bash
# 1. 从develop分支创建修复分支
git checkout develop
git pull origin develop
git checkout -b bugfix/fix-issue

# 2. 修复问题
# ... 修复代码 ...

# 3. 提交修复
git add .
git commit -m "fix: resolve issue"

# 4. 推送分支
git push origin bugfix/fix-issue

# 5. 创建Pull Request
```

### 3. 发布流程
```bash
# 1. 从develop分支创建发布分支
git checkout develop
git pull origin develop
git checkout -b release/v1.1.0

# 2. 更新版本号和CHANGELOG
./scripts/version.sh minor

# 3. 测试和修复
./test_system.py
./performance_test.py

# 4. 合并到main分支
git checkout main
git merge release/v1.1.0
git tag v1.1.0
git push origin main --tags

# 5. 合并回develop分支
git checkout develop
git merge release/v1.1.0
git push origin develop

# 6. 删除发布分支
git branch -d release/v1.1.0
git push origin --delete release/v1.1.0
```

## 📚 项目文档

### 主要文档
- [README.md](README.md) - 项目说明
- [ARCHITECTURE.md](ARCHITECTURE.md) - 架构设计
- [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API文档
- [CHANGELOG.md](CHANGELOG.md) - 更新日志

### 脚本文件
- `scripts/version.sh` - 版本管理
- `scripts/release.sh` - 发布脚本
- `scripts/setup-git.sh` - Git设置
- `scripts/team-setup.sh` - 团队设置

## 🚀 自动化设置

### 1. GitHub Actions CI/CD
项目已包含完整的CI/CD配置：
- 自动测试
- 代码质量检查
- 自动构建
- 自动部署

### 2. 代码质量检查
- Python: black, flake8, pytest
- JavaScript: ESLint, Prettier
- Java: Checkstyle, SpotBugs

### 3. 自动化部署
- Docker容器化
- 多环境部署
- 监控和告警

## 📞 支持

### 问题反馈
- 创建Issue: https://github.com/KathrynMill/agent-project2/issues
- 讨论区: https://github.com/KathrynMill/agent-project2/discussions

### 联系方式
- 项目仓库: https://github.com/KathrynMill/agent-project2
- 开发团队: Echo Command Team

---

**按照此指南设置完成后，您的项目将具备完整的版本管理和团队协作能力！** 🎉


