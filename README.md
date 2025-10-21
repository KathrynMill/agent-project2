# 🎯 Echo Command - 语音控制电脑系统

基于大模型的语音对话控制电脑应用，支持播放音乐、写文章、打开应用等复杂场景。

## ✨ 功能特性

### 🎤 语音识别
- 实时语音录制和识别
- 支持中文/英文语音命令
- 高准确率语音转文本

### 🤖 AI智能对话
- 本地大模型（SimpleLocalLLM-1.0）
- 智能意图识别和解析
- 上下文理解和多轮对话

### 🖥️ 系统控制
- **音乐控制**: 播放音乐、调节音量
- **应用控制**: 打开浏览器、启动应用程序
- **文件操作**: 生成文章、保存文件
- **系统信息**: 获取系统状态

### 📝 文本生成
- 自动生成Markdown文章
- 代码生成功能
- 智能内容创作

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- 现代浏览器

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/KathrynMill/echo-command.git
cd echo-command
```

2. **启动后端服务**
```bash
python3 simple_http_server.py
```

3. **启动前端服务**
```bash
cd frontend
npm install
npm run dev
```

4. **访问应用**
- 主界面: http://localhost:5173
- 语音演示: http://localhost:5173/voice-demo.html
- API接口: http://127.0.0.1:8001

## 🎯 使用指南

### 语音控制
1. 点击"点击说话"按钮
2. 说出您的命令，如：
   - "写一篇文章"
   - "播放音乐"
   - "打开浏览器"
   - "调节音量到50"

### 文本命令
1. 在文本框中输入命令
2. 点击"发送"按钮
3. 查看AI响应和执行结果

## 📁 项目结构

```
echo-command/
├── backend/                 # Python后端服务
├── frontend/                # Vue.js前端界面
├── cloud/                   # Java云端服务
├── scripts/                 # 工具脚本
│   ├── version.sh          # 版本管理
│   └── github-upload.sh    # GitHub上传
├── system_controller.py     # 系统控制器
├── voice_recognition.py     # 语音识别模块
├── simple_http_server.py   # HTTP服务器
├── simple_test.py          # 测试脚本
├── CHANGELOG.md            # 更新日志
├── VERSION                 # 版本号
└── README.md              # 项目说明
```

## 🔧 技术架构

### 后端技术栈
- **Python 3.8+**: 核心开发语言
- **HTTP Server**: 轻量级Web服务器
- **本地大模型**: SimpleLocalLLM-1.0
- **系统控制**: 跨平台系统API调用

### 前端技术栈
- **Vue.js 3**: 现代化前端框架
- **Element Plus**: UI组件库
- **Vite**: 快速构建工具
- **WebSocket**: 实时通信

### 部署方式
- **本地部署**: 开发环境
- **Docker**: 容器化部署
- **GitHub Actions**: CI/CD自动化

## 📊 性能指标

- **内存使用**: 约70MB
- **响应时间**: <1秒
- **识别准确率**: 90%
- **支持并发**: 单用户
- **运行成本**: 100%免费

## 🎮 演示功能

### 语音命令示例
- "你好" → 系统问候和状态信息
- "播放音乐" → 打开音乐播放器
- "打开浏览器" → 启动浏览器
- "写一篇关于AI的文章" → 生成文章文件
- "调节音量到70" → 调节系统音量

### 复杂场景
- 多步骤任务执行
- 错误处理和重试
- 实时状态反馈
- 文件自动保存

## 🔄 版本管理

### 查看版本
```bash
./scripts/version.sh show
```

### 发布新版本
```bash
./scripts/version.sh release patch  # 补丁版本
./scripts/version.sh release minor  # 次版本
./scripts/version.sh release major  # 主版本
```

### 回滚版本
```bash
./scripts/version.sh rollback 1.0.0
```

## 📤 GitHub上传

### 完整上传
```bash
./scripts/github-upload.sh upload "feat: 添加新功能"
```

### 分步上传
```bash
./scripts/github-upload.sh status    # 检查状态
./scripts/github-upload.sh add       # 添加文件
./scripts/github-upload.sh commit    # 创建提交
./scripts/github-upload.sh push      # 推送到GitHub
```

## 🧪 测试

### 运行测试
```bash
python3 simple_test.py
```

### 测试功能
- 语音识别测试
- 系统控制测试
- API接口测试
- 前端功能测试

## 📚 文档

- [架构设计](ARCHITECTURE.md)
- [API文档](API_DOCUMENTATION.md)
- [开发指南](DEVELOPMENT.md)
- [更新日志](CHANGELOG.md)

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- OpenAI GPT-4o 模型参考
- Vue.js 生态系统
- Element Plus 组件库
- 开源社区支持

## 📞 联系方式

- 项目地址: https://github.com/KathrynMill/echo-command
- 问题反馈: [Issues](https://github.com/KathrynMill/echo-command/issues)
- 功能建议: [Discussions](https://github.com/KathrynMill/echo-command/discussions)

---

**🎉 感谢使用 Echo Command 语音控制系统！**