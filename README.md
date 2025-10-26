# 🎙️ AI语音助手 - Voice Assistant

[![GitHub](https://img.shields.io/badge/GitHub-KathrynMill%2Fagent--project2-blue)](https://github.com/KathrynMill/agent-project2)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)

基于大模型的智能语音助手系统，支持通过语音或文字控制电脑完成各种任务。

> **🎓 项目背景：** 本项目为AI应用开发课程作业，要求基于大模型开发语音对话控制系统，**不使用第三方Agent框架**，仅调用LLM、ASR、TTS API，并提供详细的产品设计文档。

---

## ✨ 核心特性

### 🎯 产品功能

| 功能 | 描述 | 示例 |
|------|------|------|
| 🌐 **打开网站** | 智能识别并打开目标网站 | "帮我打开GitHub" |
| 🎵 **播放音乐** | 搜索并播放指定歌曲 | "播放周杰伦的稻香" |
| 📝 **撰写文章** | AI自动生成文章内容 | "写一篇关于AI的文章" |
| 💻 **生成代码** | 根据需求生成代码 | "用Python写一个快速排序" |
| 🔍 **网络搜索** | 快速搜索信息 | "搜索机器学习教程" |
| 🧠 **智能对话** | 自然语言交互 | "介绍一下深度学习" |

### 🏗️ 技术架构

- **🎤 语音识别**: 讯飞WebSocket ASR（支持中英混合）
- **🧠 大模型**: 七牛云DeepSeek-V3（高性能推理）
- **🔊 语音合成**: 讯飞TTS（自然语音播报）
- **🤖 智能Agent**: 自研Agent架构（意图理解→任务规划→工具调用）

---

## 🚀 快速开始

### 1️⃣ 启动服务器

```bash
cd /home/aa/echo-command
python3 voice_assistant_server.py
```

或使用启动脚本：

```bash
./scripts/start-server.sh
```

### 2️⃣ 访问Web界面

在浏览器打开：

```
http://localhost:8090/frontend/index.html
```

### 3️⃣ 开始使用

- **文本输入**: 在输入框输入指令，点击发送
- **语音输入**: 
  - 快速点击 = 浏览器实时识别
  - 长按1秒+ = 讯飞录音识别（更稳定）

💡 **新手推荐**: 点击页面上的示例卡片快速体验！

---

## 📚 完整文档

### 📖 [产品设计文档](./docs/design/产品设计.md) ⭐ 必读

回答课程要求的4个核心问题：

1. **产品功能与优先级** - 详细的功能规划和开发计划
2. **技术挑战与解决方案** - 实现过程中的难点和应对策略
3. **LLM模型选型对比** - 为什么选择DeepSeek-V3
4. **未来规划** - 产品的演进方向和扩展能力

### 📖 其他文档

| 文档 | 说明 |
|------|------|
| [📁 文档中心](./docs/) | 所有文档导航 |
| [🚀 快速开始](./docs/user-guide/快速开始.md) | 5分钟快速上手 |
| [📖 使用手册](./docs/user-guide/使用手册.md) | 详细使用说明 |
| [🎤 语音功能说明](./docs/user-guide/语音功能说明.md) | 语音识别使用指南 |
| [🏗️ 项目状态](./docs/design/项目状态.md) | 当前开发进度 |
| [🐛 修复记录](./docs/development/修复记录.md) | Bug修复历史 |
| [📝 变更日志](./CHANGELOG.md) | 版本更新记录 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────┐
│                   用户界面 (Web)                      │
│            语音输入 + 文字输入 + 示例卡片              │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              语音助手服务器 (Python)                   │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │   API客户端   │  │ 智能Agent    │  │系统控制器 │ │
│  │              │  │              │  │          │ │
│  │• 讯飞ASR     │  │• 意图理解    │  │• 网站    │ │
│  │• 七牛LLM     │  │• 任务规划    │  │• 音乐    │ │
│  │• 讯飞TTS     │  │• 工具调用    │  │• 文件    │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
echo-command/
├── README.md                    # 项目主页（本文件）
├── CHANGELOG.md                 # 版本变更记录
│
├── docs/                        # 📚 文档中心
│   ├── design/                  # 设计文档
│   │   ├── 产品设计.md          # ⭐ 核心设计文档
│   │   └── 项目状态.md
│   ├── user-guide/              # 用户指南
│   │   ├── 快速开始.md
│   │   ├── 使用手册.md
│   │   └── 语音功能说明.md
│   └── development/             # 开发文档
│       └── 修复记录.md
│
├── scripts/                     # 🔧 工具脚本
│   ├── start-server.sh          # 启动服务器
│   ├── git-commit.sh            # 专业Git提交
│   └── quick-commit.sh          # 快速提交
│
├── frontend/                    # 🎨 前端界面
│   └── index.html               # 现代化Web界面
│
├── voice_assistant_server.py    # 🚀 主服务器
├── intelligent_agent.py         # 🤖 自研Agent
├── system_controller.py         # 🎮 系统控制器
├── qiniu_api_client.py          # 🧠 七牛云LLM客户端
├── xunfei_client.py             # 🎤 讯飞语音客户端
├── xunfei_asr_official.py       # 🎙️ 讯飞ASR实现
└── baidu_api_client.py          # 🔧 百度API客户端（备用）
```

---

## 🎯 核心实现亮点

### 1. 自研Agent架构 ⭐

**不使用LangChain等第三方框架**，完全自主实现：

- **意图理解 (Intent Understanding)**: 使用LLM深度语义分析
- **任务规划 (Task Planning)**: 自动分解复杂任务
- **工具调用 (Tool Calling)**: 动态选择和执行工具

### 2. 多API集成

| API提供商 | 用途 | 选择理由 |
|----------|------|---------|
| **七牛云** | LLM (DeepSeek-V3) | 性能强、成本低、API稳定 |
| **讯飞** | ASR + TTS | 中文识别准确、响应快速 |
| 百度 | 备用LLM | 文心一言（可选） |

### 3. 现代化UI设计

- 🎨 深色主题 + 玻璃态设计
- ✨ 炫酷动画效果
- 📱 响应式布局
- 🎯 直观的交互体验

---

## 🔑 API配置

### 讯飞语音服务（已配置）

系统已配置讯飞ASR和TTS，开箱即用。

### 七牛云LLM（已配置）

使用七牛云DeepSeek-V3模型，已在代码中配置。

### 自定义配置

如需使用自己的API Key，编辑 `voice_assistant_server.py`:

```python
# 七牛云LLM
qiniu_api_key = "your-api-key-here"

# 讯飞语音
xunfei_client = XunfeiClient(
    appid="your-appid",
    api_key="your-api-key",
    api_secret="your-api-secret"
)
```

---

## 🛠️ Git工具使用

### 专业提交（推荐）

```bash
./scripts/git-commit.sh
```

功能：
- ✅ 交互式选择提交类型
- ✅ 自动生成CHANGELOG
- ✅ 支持版本标签
- ✅ 提供回滚功能

### 快速提交

```bash
./scripts/quick-commit.sh "提交说明"
```

---

## 📊 API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/text` | POST | 文本输入处理 |
| `/api/voice` | POST | 语音输入处理 |
| `/api/tts` | POST | 文字转语音 |
| `/api/chat` | POST | 纯对话 |
| `/health` | GET | 健康检查 |

---

## 🧪 测试示例

### 测试文本输入

```bash
curl -X POST http://localhost:8090/api/text \
  -H "Content-Type: application/json" \
  -d '{"text": "帮我打开GitHub"}'
```

### 测试健康检查

```bash
curl http://localhost:8090/health
```

---

## 📝 开发规范

### Git提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 代码规范

- 使用PEP 8编码规范
- 函数添加类型注解
- 重要逻辑添加注释
- 保持代码简洁易读

---

## 🤝 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`./scripts/git-commit.sh`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

---

## 📄 许可证

本项目为AI应用开发课程作业项目。

---

## 👨‍💻 作者

**KathrynMill**

- GitHub: [@KathrynMill](https://github.com/KathrynMill)
- 项目: [agent-project2](https://github.com/KathrynMill/agent-project2)

---

## 🙏 致谢

- 七牛云提供高性能LLM API
- 讯飞提供准确的语音识别和合成服务
- 所有开源项目和社区的支持

---

## 📞 联系方式

- 📧 Issues: [GitHub Issues](https://github.com/KathrynMill/agent-project2/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/KathrynMill/agent-project2/discussions)

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给一个Star！**

Made with ❤️ by KathrynMill

*最后更新: 2025-10-26*

</div>
