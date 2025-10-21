<template>
  <div class="settings-page">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" class="settings-tabs">
        <!-- 连接设置 -->
        <el-tab-pane label="连接设置" name="connection">
          <div class="settings-section">
            <h3>WebSocket连接</h3>
            <el-form :model="connectionSettings" label-width="120px">
              <el-form-item label="服务器地址">
                <el-input v-model="connectionSettings.host" placeholder="127.0.0.1" />
              </el-form-item>
              <el-form-item label="端口">
                <el-input-number v-model="connectionSettings.port" :min="1" :max="65535" />
              </el-form-item>
              <el-form-item label="自动重连">
                <el-switch v-model="connectionSettings.autoReconnect" />
              </el-form-item>
              <el-form-item label="重连间隔(秒)">
                <el-input-number 
                  v-model="connectionSettings.reconnectInterval" 
                  :min="1" 
                  :max="60"
                  :disabled="!connectionSettings.autoReconnect"
                />
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
        
        <!-- 音频设置 -->
        <el-tab-pane label="音频设置" name="audio">
          <div class="settings-section">
            <h3>录音设置</h3>
            <el-form :model="audioSettings" label-width="120px">
              <el-form-item label="采样率">
                <el-select v-model="audioSettings.sampleRate">
                  <el-option label="16000 Hz" :value="16000" />
                  <el-option label="44100 Hz" :value="44100" />
                  <el-option label="48000 Hz" :value="48000" />
                </el-select>
              </el-form-item>
              <el-form-item label="声道数">
                <el-radio-group v-model="audioSettings.channels">
                  <el-radio :label="1">单声道</el-radio>
                  <el-radio :label="2">立体声</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="回声消除">
                <el-switch v-model="audioSettings.echoCancellation" />
              </el-form-item>
              <el-form-item label="噪声抑制">
                <el-switch v-model="audioSettings.noiseSuppression" />
              </el-form-item>
            </el-form>
            
            <h3>TTS设置</h3>
            <el-form :model="ttsSettings" label-width="120px">
              <el-form-item label="语速">
                <el-slider 
                  v-model="ttsSettings.rate" 
                  :min="50" 
                  :max="300" 
                  :step="10"
                  show-input
                />
              </el-form-item>
              <el-form-item label="音量">
                <el-slider 
                  v-model="ttsSettings.volume" 
                  :min="0" 
                  :max="1" 
                  :step="0.1"
                  show-input
                />
              </el-form-item>
              <el-form-item label="语音">
                <el-select v-model="ttsSettings.voice" placeholder="选择语音">
                  <el-option 
                    v-for="voice in availableVoices" 
                    :key="voice.id" 
                    :label="voice.name" 
                    :value="voice.id" 
                  />
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
        
        <!-- AI设置 -->
        <el-tab-pane label="AI设置" name="ai">
          <div class="settings-section">
            <h3>OpenAI配置</h3>
            <el-form :model="aiSettings" label-width="120px">
              <el-form-item label="API Key">
                <el-input 
                  v-model="aiSettings.apiKey" 
                  type="password" 
                  show-password
                  placeholder="输入OpenAI API Key"
                />
              </el-form-item>
              <el-form-item label="模型">
                <el-select v-model="aiSettings.model">
                  <el-option label="GPT-4o" value="gpt-4o" />
                  <el-option label="GPT-4" value="gpt-4" />
                  <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
                </el-select>
              </el-form-item>
              <el-form-item label="温度">
                <el-slider 
                  v-model="aiSettings.temperature" 
                  :min="0" 
                  :max="2" 
                  :step="0.1"
                  show-input
                />
              </el-form-item>
              <el-form-item label="最大令牌数">
                <el-input-number 
                  v-model="aiSettings.maxTokens" 
                  :min="1" 
                  :max="4096" 
                />
              </el-form-item>
            </el-form>
            
            <h3>语音识别设置</h3>
            <el-form :model="sttSettings" label-width="120px">
              <el-form-item label="语言">
                <el-select v-model="sttSettings.language">
                  <el-option label="中文" value="zh-CN" />
                  <el-option label="英文" value="en-US" />
                  <el-option label="日文" value="ja-JP" />
                  <el-option label="韩文" value="ko-KR" />
                </el-select>
              </el-form-item>
              <el-form-item label="模型大小">
                <el-select v-model="sttSettings.modelSize">
                  <el-option label="Tiny" value="tiny" />
                  <el-option label="Base" value="base" />
                  <el-option label="Small" value="small" />
                  <el-option label="Medium" value="medium" />
                  <el-option label="Large" value="large" />
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
        
        <!-- 系统设置 -->
        <el-tab-pane label="系统设置" name="system">
          <div class="settings-section">
            <h3>系统控制</h3>
            <el-form :model="systemSettings" label-width="120px">
              <el-form-item label="安全模式">
                <el-switch v-model="systemSettings.safetyMode" />
                <div class="setting-description">
                  启用后，系统控制命令需要确认才能执行
                </div>
              </el-form-item>
              <el-form-item label="命令延迟(秒)">
                <el-input-number 
                  v-model="systemSettings.commandDelay" 
                  :min="0" 
                  :max="5" 
                  :step="0.1"
                />
              </el-form-item>
              <el-form-item label="自动截图">
                <el-switch v-model="systemSettings.autoScreenshot" />
              </el-form-item>
              <el-form-item label="日志级别">
                <el-select v-model="systemSettings.logLevel">
                  <el-option label="DEBUG" value="DEBUG" />
                  <el-option label="INFO" value="INFO" />
                  <el-option label="WARNING" value="WARNING" />
                  <el-option label="ERROR" value="ERROR" />
                </el-select>
              </el-form-item>
            </el-form>
            
            <h3>界面设置</h3>
            <el-form :model="uiSettings" label-width="120px">
              <el-form-item label="主题">
                <el-radio-group v-model="uiSettings.theme">
                  <el-radio label="light">浅色</el-radio>
                  <el-radio label="dark">深色</el-radio>
                  <el-radio label="auto">自动</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="语言">
                <el-select v-model="uiSettings.language">
                  <el-option label="中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                </el-select>
              </el-form-item>
              <el-form-item label="启动时最小化">
                <el-switch v-model="uiSettings.startMinimized" />
              </el-form-item>
              <el-form-item label="开机自启">
                <el-switch v-model="uiSettings.autoStart" />
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
      
      <!-- 操作按钮 -->
      <div class="settings-actions">
        <el-button @click="resetSettings">重置设置</el-button>
        <el-button @click="exportSettings">导出设置</el-button>
        <el-button @click="importSettings">导入设置</el-button>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Setting } from '@element-plus/icons-vue'

const activeTab = ref('connection')

// 连接设置
const connectionSettings = reactive({
  host: '127.0.0.1',
  port: 8000,
  autoReconnect: true,
  reconnectInterval: 5
})

// 音频设置
const audioSettings = reactive({
  sampleRate: 16000,
  channels: 1,
  echoCancellation: true,
  noiseSuppression: true
})

const ttsSettings = reactive({
  rate: 200,
  volume: 0.9,
  voice: 0
})

const availableVoices = ref([
  { id: 0, name: '默认语音' },
  { id: 1, name: '女声' },
  { id: 2, name: '男声' }
])

// AI设置
const aiSettings = reactive({
  apiKey: '',
  model: 'gpt-4o',
  temperature: 0.1,
  maxTokens: 1000
})

const sttSettings = reactive({
  language: 'zh-CN',
  modelSize: 'base'
})

// 系统设置
const systemSettings = reactive({
  safetyMode: true,
  commandDelay: 0.1,
  autoScreenshot: false,
  logLevel: 'INFO'
})

const uiSettings = reactive({
  theme: 'light',
  language: 'zh-CN',
  startMinimized: false,
  autoStart: false
})

// 方法
function loadSettings() {
  // 从本地存储加载设置
  const settings = localStorage.getItem('echo-command-settings')
  if (settings) {
    try {
      const parsed = JSON.parse(settings)
      Object.assign(connectionSettings, parsed.connection || {})
      Object.assign(audioSettings, parsed.audio || {})
      Object.assign(ttsSettings, parsed.tts || {})
      Object.assign(aiSettings, parsed.ai || {})
      Object.assign(sttSettings, parsed.stt || {})
      Object.assign(systemSettings, parsed.system || {})
      Object.assign(uiSettings, parsed.ui || {})
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }
}

function saveSettings() {
  try {
    const settings = {
      connection: connectionSettings,
      audio: audioSettings,
      tts: ttsSettings,
      ai: aiSettings,
      stt: sttSettings,
      system: systemSettings,
      ui: uiSettings
    }
    
    localStorage.setItem('echo-command-settings', JSON.stringify(settings))
    ElMessage.success('设置保存成功')
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  }
}

function resetSettings() {
  ElMessageBox.confirm(
    '确定要重置所有设置吗？此操作不可撤销。',
    '确认重置',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    localStorage.removeItem('echo-command-settings')
    loadSettings()
    ElMessage.success('设置已重置')
  }).catch(() => {
    // 用户取消
  })
}

function exportSettings() {
  try {
    const settings = {
      connection: connectionSettings,
      audio: audioSettings,
      tts: ttsSettings,
      ai: aiSettings,
      stt: sttSettings,
      system: systemSettings,
      ui: uiSettings
    }
    
    const dataStr = JSON.stringify(settings, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    
    const link = document.createElement('a')
    link.href = URL.createObjectURL(dataBlob)
    link.download = 'echo-command-settings.json'
    link.click()
    
    ElMessage.success('设置导出成功')
  } catch (error) {
    console.error('导出设置失败:', error)
    ElMessage.error('导出设置失败')
  }
}

function importSettings() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  
  input.onchange = (event) => {
    const file = event.target.files[0]
    if (!file) return
    
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const settings = JSON.parse(e.target.result)
        
        Object.assign(connectionSettings, settings.connection || {})
        Object.assign(audioSettings, settings.audio || {})
        Object.assign(ttsSettings, settings.tts || {})
        Object.assign(aiSettings, settings.ai || {})
        Object.assign(sttSettings, settings.stt || {})
        Object.assign(systemSettings, settings.system || {})
        Object.assign(uiSettings, settings.ui || {})
        
        ElMessage.success('设置导入成功')
      } catch (error) {
        console.error('导入设置失败:', error)
        ElMessage.error('导入设置失败')
      }
    }
    
    reader.readAsText(file)
  }
  
  input.click()
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.settings-page {
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.settings-card {
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}

.settings-tabs {
  margin-bottom: 20px;
}

.settings-section {
  padding: 20px 0;
}

.settings-section h3 {
  margin-bottom: 20px;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 8px;
}

.setting-description {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-page {
    padding: 10px;
  }
  
  .settings-actions {
    flex-direction: column;
  }
  
  .settings-actions .el-button {
    width: 100%;
  }
}
</style>

