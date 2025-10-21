# Echo Command - 开发指南

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- Java 17+ (云端服务)
- Docker (可选)
- Git

### 克隆项目
```bash
git clone https://github.com/KathrynMill/agent-project2.git
cd agent-project2
```

### 设置开发环境
```bash
# 运行团队设置脚本
./scripts/team-setup.sh your-name

# 或手动设置
./install.sh
```

## 📁 项目结构

```
echo-command/
├── 📁 backend/              # Python后端服务
│   ├── 📁 config/           # 配置管理
│   ├── 📁 models/           # 数据模型
│   ├── 📁 services/         # 业务服务
│   │   ├── 📁 ai/           # AI服务
│   │   └── 📁 system/       # 系统控制
│   ├── 📄 main.py           # 主应用
│   ├── 📄 requirements.txt  # Python依赖
│   └── 📄 Dockerfile        # Docker配置
├── 📁 frontend/             # Electron前端应用
│   ├── 📁 src/              # 源代码
│   │   ├── 📁 components/   # 组件
│   │   ├── 📁 views/        # 页面
│   │   ├── 📁 stores/       # 状态管理
│   │   └── 📁 services/     # 服务层
│   ├── 📁 public/           # 静态资源
│   ├── 📄 package.json      # 项目配置
│   └── 📄 Dockerfile        # Docker配置
├── 📁 cloud/                # Java云端服务
│   ├── 📁 src/              # 源代码
│   ├── 📄 pom.xml           # Maven配置
│   └── 📄 Dockerfile        # Docker配置
├── 📁 scripts/              # 脚本文件
│   ├── 📄 version.sh        # 版本管理
│   ├── 📄 release.sh        # 发布脚本
│   ├── 📄 setup-git.sh      # Git设置
│   └── 📄 team-setup.sh     # 团队设置
├── 📁 monitoring/           # 监控配置
├── 📁 .github/              # CI/CD配置
├── 📄 docker-compose.yml    # 容器编排
├── 📄 VERSION               # 版本号
└── 📄 CHANGELOG.md          # 更新日志
```

## 🔧 开发流程

### 1. 分支管理
```bash
# 主分支
main          # 生产环境代码
develop       # 开发环境代码

# 功能分支
feature/xxx   # 新功能开发
bugfix/xxx    # 问题修复
hotfix/xxx    # 紧急修复
```

### 2. 开发步骤
```bash
# 1. 创建功能分支
git checkout -b feature/your-feature-name

# 2. 开发功能
# ... 编写代码 ...

# 3. 提交代码
git add .
git commit -m "feat: add new feature"

# 4. 推送分支
git push origin feature/your-feature-name

# 5. 创建Pull Request
# 在GitHub上创建PR，请求合并到develop分支
```

### 3. 代码规范

#### Python代码规范
```python
# 使用black格式化
black backend/

# 使用flake8检查
flake8 backend/

# 类型注解
def process_audio(audio_data: bytes, sample_rate: int) -> str:
    """处理音频数据"""
    pass
```

#### JavaScript/Vue代码规范
```javascript
// 使用ESLint检查
npm run lint

// 组件命名使用PascalCase
export default {
  name: 'AudioVisualizer'
}

// 函数命名使用camelCase
const processAudioData = () => {
  // ...
}
```

#### Java代码规范
```java
// 使用Google Java Style
// 类名使用PascalCase
public class UserService {
    
    // 方法名使用camelCase
    public UserDto getUserById(Long id) {
        // ...
    }
}
```

## 🧪 测试

### 运行测试
```bash
# 系统测试
./test_system.py

# 性能测试
./performance_test.py

# 后端测试
cd backend
python -m pytest tests/

# 前端测试
cd frontend
npm test

# 云端服务测试
cd cloud
mvn test
```

### 测试覆盖率
```bash
# Python测试覆盖率
cd backend
pytest --cov=. --cov-report=html

# JavaScript测试覆盖率
cd frontend
npm run test:coverage
```

## 🚀 部署

### 本地开发
```bash
# 启动后端
cd backend
source venv/bin/activate
python main.py

# 启动前端
cd frontend
npm run electron:dev

# 启动云端服务
cd cloud
mvn spring-boot:run
```

### Docker部署
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 生产部署
```bash
# 一键部署
./deploy.sh

# 或手动部署
./scripts/release.sh patch
```

## 📊 监控和调试

### 日志查看
```bash
# 查看应用日志
tail -f logs/echo_command.log

# 查看Docker日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f cloud-service
```

### 性能监控
```bash
# 访问监控面板
http://localhost:3000  # Grafana
http://localhost:9090  # Prometheus

# 查看API文档
http://localhost:8080/swagger-ui.html
```

## 🔄 版本管理

### 版本号规则
- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

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

## 🐛 问题排查

### 常见问题

#### 1. 后端启动失败
```bash
# 检查Python版本
python3 --version

# 检查依赖安装
cd backend
pip install -r requirements.txt

# 检查环境变量
cat .env
```

#### 2. 前端启动失败
```bash
# 检查Node.js版本
node --version

# 重新安装依赖
cd frontend
rm -rf node_modules
npm install
```

#### 3. 云端服务启动失败
```bash
# 检查Java版本
java --version

# 检查Maven配置
cd cloud
mvn clean install
```

#### 4. Docker部署问题
```bash
# 检查Docker状态
docker --version
docker-compose --version

# 重新构建镜像
docker-compose build --no-cache

# 清理容器
docker-compose down
docker system prune -f
```

### 调试技巧

#### 1. 日志级别调整
```bash
# 后端日志级别
export LOG_LEVEL=DEBUG

# 前端调试模式
cd frontend
npm run electron:dev -- --debug
```

#### 2. 网络问题排查
```bash
# 检查端口占用
netstat -tulpn | grep :8000
netstat -tulpn | grep :8080

# 检查防火墙
sudo ufw status
```

#### 3. 数据库连接问题
```bash
# 检查MySQL连接
mysql -h localhost -u root -p

# 检查Redis连接
redis-cli ping
```

## 📚 文档

### 项目文档
- [README.md](README.md) - 项目说明
- [ARCHITECTURE.md](ARCHITECTURE.md) - 架构设计
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API文档
- [CHANGELOG.md](CHANGELOG.md) - 更新日志

### 外部文档
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Vue.js文档](https://vuejs.org/)
- [Spring Boot文档](https://spring.io/projects/spring-boot)
- [Docker文档](https://docs.docker.com/)

## 🤝 贡献指南

### 提交规范
```
feat: 新功能
fix: 问题修复
docs: 文档更新
style: 代码格式
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### Pull Request规范
1. 标题清晰描述变更内容
2. 详细描述变更原因和影响
3. 关联相关Issue
4. 确保所有测试通过
5. 更新相关文档

### 代码审查
1. 功能正确性
2. 代码可读性
3. 性能影响
4. 安全性考虑
5. 测试覆盖率

## 📞 联系方式

- 项目仓库: https://github.com/KathrynMill/agent-project2
- 问题反馈: https://github.com/KathrynMill/agent-project2/issues
- 讨论区: https://github.com/KathrynMill/agent-project2/discussions
- 开发团队: Echo Command Team

---

**Happy Coding! 🎉**
