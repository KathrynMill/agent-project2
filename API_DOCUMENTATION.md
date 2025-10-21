# Echo Command API 文档

## 概述

Echo Command 提供两套API服务：
- **本地后端API** (Python FastAPI): 实时AI处理和系统控制
- **云端服务API** (Java Spring Boot): 用户管理和数据持久化

## 本地后端API (端口: 8000)

### 基础信息
- **Base URL**: `http://localhost:8000`
- **协议**: HTTP/WebSocket
- **认证**: 无需认证（本地服务）

### WebSocket接口

#### 连接WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

#### 消息格式

**音频消息**
```json
{
  "type": "audio",
  "audio_data": "base64_encoded_audio_data",
  "sample_rate": 16000,
  "session_id": "optional_session_id"
}
```

**文本消息**
```json
{
  "type": "text",
  "text": "用户输入的文本",
  "session_id": "optional_session_id"
}
```

**命令消息**
```json
{
  "type": "command",
  "command_type": "system_control",
  "action": "volume_set",
  "parameters": {
    "volume": 50
  },
  "session_id": "optional_session_id"
}
```

**心跳消息**
```json
{
  "type": "heartbeat",
  "session_id": "optional_session_id"
}
```

#### 响应格式

**成功响应**
```json
{
  "type": "response",
  "success": true,
  "message": "操作成功",
  "data": {
    "transcription": "识别的文本",
    "intent": "解析的意图",
    "execution_time": 0.5
  },
  "audio_response": "hex_encoded_audio_data",
  "session_id": "session_id"
}
```

**错误响应**
```json
{
  "type": "error",
  "error_code": "ERROR_CODE",
  "error_message": "错误描述",
  "session_id": "session_id"
}
```

### HTTP接口

#### 健康检查
```http
GET /health
```

**响应**
```json
{
  "status": "healthy",
  "timestamp": 1640995200.0,
  "active_connections": 5,
  "sessions": {
    "total_sessions": 10,
    "active_sessions": 5,
    "total_commands": 100
  }
}
```

#### 获取会话列表
```http
GET /api/sessions
```

#### 创建会话
```http
POST /api/sessions
```

#### 删除会话
```http
DELETE /api/sessions/{session_id}
```

## 云端服务API (端口: 8080)

### 基础信息
- **Base URL**: `http://localhost:8080/api`
- **协议**: HTTP
- **认证**: JWT Token
- **文档**: `http://localhost:8080/swagger-ui.html`

### 认证接口

#### 用户注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123",
  "nickname": "用户昵称"
}
```

**响应**
```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "nickname": "用户昵称"
  }
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "user123",
  "password": "password123"
}
```

#### 刷新令牌
```http
POST /api/auth/refresh?refresh_token=jwt_refresh_token
```

#### 用户登出
```http
POST /api/auth/logout?refresh_token=jwt_refresh_token
```

### 用户管理接口

#### 获取用户信息
```http
GET /api/users/profile
Authorization: Bearer jwt_access_token
```

#### 更新用户信息
```http
PUT /api/users/profile
Authorization: Bearer jwt_access_token
Content-Type: application/json

{
  "nickname": "新昵称",
  "avatar": "avatar_url"
}
```

#### 获取用户设置
```http
GET /api/users/settings
Authorization: Bearer jwt_access_token
```

#### 更新用户设置
```http
PUT /api/users/settings
Authorization: Bearer jwt_access_token
Content-Type: application/json

{
  "theme": "dark",
  "language": "zh-CN",
  "tts_rate": 200,
  "tts_volume": 0.9
}
```

### 自定义命令接口

#### 获取命令列表
```http
GET /api/commands?page=0&size=10
Authorization: Bearer jwt_access_token
```

#### 获取公共命令
```http
GET /api/commands/public?page=0&size=10
```

#### 创建命令
```http
POST /api/commands
Authorization: Bearer jwt_access_token
Content-Type: application/json

{
  "name": "打开浏览器",
  "description": "打开默认浏览器",
  "triggerPhrase": "打开浏览器",
  "commandScript": "open_application('browser')",
  "commandType": "APPLICATION",
  "isPublic": false
}
```

#### 获取命令详情
```http
GET /api/commands/{id}
Authorization: Bearer jwt_access_token
```

#### 更新命令
```http
PUT /api/commands/{id}
Authorization: Bearer jwt_access_token
Content-Type: application/json

{
  "name": "打开浏览器",
  "description": "打开默认浏览器",
  "triggerPhrase": "打开浏览器",
  "commandScript": "open_application('browser')",
  "commandType": "APPLICATION",
  "isPublic": true
}
```

#### 删除命令
```http
DELETE /api/commands/{id}
Authorization: Bearer jwt_access_token
```

#### 使用命令
```http
POST /api/commands/{id}/use
Authorization: Bearer jwt_access_token
```

## 错误码说明

### 本地后端错误码
- `UNKNOWN_MESSAGE_TYPE`: 未知消息类型
- `MESSAGE_HANDLING_ERROR`: 消息处理错误
- `AUDIO_PROCESSING_ERROR`: 音频处理错误
- `TEXT_PROCESSING_ERROR`: 文本处理错误
- `COMMAND_EXECUTION_ERROR`: 命令执行错误

### 云端服务错误码
- `USER_NOT_FOUND`: 用户不存在
- `INVALID_CREDENTIALS`: 无效凭据
- `TOKEN_EXPIRED`: 令牌过期
- `ACCESS_DENIED`: 访问被拒绝
- `RESOURCE_NOT_FOUND`: 资源不存在
- `VALIDATION_ERROR`: 验证错误

## 使用示例

### JavaScript WebSocket客户端

```javascript
class EchoCommandClient {
  constructor() {
    this.ws = null;
    this.sessionId = null;
  }
  
  connect() {
    this.ws = new WebSocket('ws://localhost:8000/ws');
    
    this.ws.onopen = () => {
      console.log('WebSocket连接已建立');
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket错误:', error);
    };
  }
  
  sendAudio(audioData) {
    const message = {
      type: 'audio',
      audio_data: audioData,
      sample_rate: 16000,
      session_id: this.sessionId
    };
    this.ws.send(JSON.stringify(message));
  }
  
  sendText(text) {
    const message = {
      type: 'text',
      text: text,
      session_id: this.sessionId
    };
    this.ws.send(JSON.stringify(message));
  }
  
  handleMessage(message) {
    switch (message.type) {
      case 'response':
        console.log('AI响应:', message.message);
        if (message.audio_response) {
          this.playAudio(message.audio_response);
        }
        break;
      case 'error':
        console.error('错误:', message.error_message);
        break;
    }
  }
  
  playAudio(audioHex) {
    // 播放音频响应
    const audioData = new Uint8Array(
      audioHex.match(/.{2}/g).map(byte => parseInt(byte, 16))
    );
    const audioBlob = new Blob([audioData], { type: 'audio/wav' });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
  }
}

// 使用示例
const client = new EchoCommandClient();
client.connect();
```

### Python HTTP客户端

```python
import requests
import json

class EchoCommandCloudClient:
    def __init__(self, base_url="http://localhost:8080/api"):
        self.base_url = base_url
        self.access_token = None
    
    def register(self, username, email, password, nickname=None):
        url = f"{self.base_url}/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "nickname": nickname
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.access_token = result["access_token"]
            return result
        return None
    
    def login(self, username, password):
        url = f"{self.base_url}/auth/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.access_token = result["access_token"]
            return result
        return None
    
    def get_headers(self):
        if not self.access_token:
            raise Exception("未登录")
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def get_profile(self):
        url = f"{self.base_url}/users/profile"
        response = requests.get(url, headers=self.get_headers())
        return response.json() if response.status_code == 200 else None
    
    def create_command(self, name, trigger_phrase, command_script, command_type="CUSTOM"):
        url = f"{self.base_url}/commands"
        data = {
            "name": name,
            "triggerPhrase": trigger_phrase,
            "commandScript": command_script,
            "commandType": command_type
        }
        response = requests.post(url, json=data, headers=self.get_headers())
        return response.json() if response.status_code == 200 else None

# 使用示例
client = EchoCommandCloudClient()
client.login("user123", "password123")
profile = client.get_profile()
print(profile)
```

## 部署说明

### 本地开发
```bash
# 启动后端
cd backend
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

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 生产部署
```bash
# 设置环境变量
export OPENAI_API_KEY=your_api_key
export DB_PASSWORD=your_db_password
export JWT_SECRET=your_jwt_secret

# 部署
./deploy.sh
```



