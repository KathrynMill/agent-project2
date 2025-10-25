# 更新日志 (Changelog)

## [v2.0.0] - 2025-10-25

### 🎉 重大更新

#### ✨ 新增功能
- **讯飞语音识别集成** - 集成讯飞WebSocket ASR，支持实时语音识别
- **七牛云LLM集成** - 使用DeepSeek-V3大模型进行智能理解
- **自研Agent系统** - 实现意图识别、任务规划、工具调用
- **系统控制器** - 支持打开网站、播放音乐、写文章、生成代码等功能
- **Web前端界面** - 美观的语音交互界面
- **中英文混合识别** - 支持"打开GitHub"等中英混合指令

#### 🔧 技术改进
- 采用讯飞官方Demo实现，更稳定可靠
- 支持多种API客户端（讯飞、七牛云、百度）
- 前端WAV音频录制，符合ASR要求
- 完善的错误处理和用户提示
- 详细的文档和使用说明

#### 📝 核心文件
- `voice_assistant_server.py` - 主服务器
- `intelligent_agent.py` - 智能Agent
- `system_controller.py` - 系统控制器
- `xunfei_asr_official.py` - 讯飞ASR客户端
- `qiniu_api_client.py` - 七牛云API客户端
- `frontend/index.html` - Web界面

#### 🗑️ 清理
- 删除冗余的Node.js文件和目录
- 删除旧版本的测试文件
- 删除不再使用的脚本

#### 📚 文档
- `README.md` - 项目说明
- `PROJECT_STATUS.md` - 项目状态
- `使用说明.md` - 使用手册
- `语音识别方案对比.md` - 方案对比
- `讯飞配置说明.md` - 配置指南

### 🎓 项目特点
- ✅ 满足课程要求：调用LLM API、ASR API、TTS API
- ✅ 不使用第三方Agent框架，完全自研
- ✅ 真实的大模型智能理解
- ✅ 实际的系统控制功能
- ✅ 完整的语音交互体验

### 🚀 快速开始
```bash
# 启动服务器
python3 voice_assistant_server.py

# 打开浏览器访问
http://localhost:8090/frontend/
```

---

## [v1.0.0] - 之前版本
- 初始版本
- 基础HTTP服务器
- 简单的规则匹配

