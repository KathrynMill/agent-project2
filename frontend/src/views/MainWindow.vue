<template>
  <div class="main-window">
    <!-- 状态栏 -->
    <div class="status-bar">
      <div class="status-info">
        <el-icon :class="statusIconClass">
          <component :is="statusIcon" />
        </el-icon>
        <span class="status-text">{{ sessionStore.statusText }}</span>
      </div>
      
      <div class="connection-status">
        <el-icon :class="connectionIconClass">
          <component :is="connectionIcon" />
        </el-icon>
        <span>{{ sessionStore.isConnected ? '已连接' : '未连接' }}</span>
      </div>
    </div>
    
    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 控制面板 -->
      <div class="control-panel">
        <el-card class="control-card">
          <template #header>
            <div class="card-header">
              <span>语音控制</span>
              <el-button 
                type="primary" 
                :loading="sessionStore.isProcessing"
                :disabled="!sessionStore.canStartListening"
                @click="toggleListening"
              >
                <el-icon>
                  <component :is="sessionStore.isListening ? 'Microphone' : 'Close'" />
                </el-icon>
                {{ sessionStore.isListening ? '停止聆听' : '开始聆听' }}
              </el-button>
            </div>
          </template>
          
          <div class="voice-control">
            <div class="voice-visualizer" :class="{ active: sessionStore.isListening }">
              <div class="wave"></div>
              <div class="wave"></div>
              <div class="wave"></div>
              <div class="wave"></div>
              <div class="wave"></div>
            </div>
            
            <p class="voice-hint">
              {{ sessionStore.isListening ? '请说话...' : '点击按钮开始语音控制' }}
            </p>
          </div>
        </el-card>
        
        <!-- 文本输入 -->
        <el-card class="text-input-card">
          <template #header>
            <span>文本输入</span>
          </template>
          
          <div class="text-input-area">
            <el-input
              v-model="inputText"
              type="textarea"
              :rows="3"
              placeholder="输入文本指令..."
              :disabled="sessionStore.isProcessing"
            />
            <el-button 
              type="primary" 
              :loading="sessionStore.isProcessing"
              :disabled="!inputText.trim() || !sessionStore.isConnected"
              @click="sendTextMessage"
              class="send-button"
            >
              发送
            </el-button>
          </div>
        </el-card>
      </div>
      
      <!-- 响应区域 -->
      <div class="response-area">
        <el-card class="response-card">
          <template #header>
            <div class="card-header">
              <span>AI响应</span>
              <el-button 
                type="text" 
                @click="clearResponse"
                :disabled="!sessionStore.responseText"
              >
                清空
              </el-button>
            </div>
          </template>
          
          <div class="response-content">
            <div v-if="sessionStore.responseText" class="response-text">
              {{ sessionStore.responseText }}
            </div>
            <div v-else class="response-placeholder">
              等待AI响应...
            </div>
          </div>
        </el-card>
        
        <!-- 错误信息 -->
        <el-alert
          v-if="sessionStore.errorMessage"
          :title="sessionStore.errorMessage"
          type="error"
          :closable="true"
          @close="sessionStore.clearError"
          class="error-alert"
        />
      </div>
    </div>
    
    <!-- 历史记录 -->
    <div class="history-section">
      <el-card class="history-card">
        <template #header>
          <div class="card-header">
            <span>命令历史</span>
            <el-button 
              type="text" 
              @click="sessionStore.clearHistory"
              :disabled="sessionStore.commandHistory.length === 0"
            >
              清空历史
            </el-button>
          </div>
        </template>
        
        <div class="history-list">
          <div 
            v-for="item in sessionStore.commandHistory" 
            :key="item.id"
            class="history-item"
            :class="{ success: item.success, error: !item.success }"
          >
            <div class="history-time">
              {{ formatTime(item.timestamp) }}
            </div>
            <div class="history-input">
              <strong>输入:</strong> {{ item.input }}
            </div>
            <div class="history-output">
              <strong>输出:</strong> {{ item.output }}
            </div>
          </div>
          
          <div v-if="sessionStore.commandHistory.length === 0" class="empty-history">
            暂无历史记录
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSessionStore } from '../stores/sessionStore'
import { 
  Microphone, 
  Close,
  Connection, 
  Loading,
  Check,
  CloseBold
} from '@element-plus/icons-vue'

const sessionStore = useSessionStore()
const inputText = ref('')

// 计算属性
const statusIcon = computed(() => {
  if (sessionStore.isProcessing) return Loading
  if (sessionStore.isListening) return Microphone
  return Close
})

const statusIconClass = computed(() => {
  if (sessionStore.isProcessing) return 'status-icon processing'
  if (sessionStore.isListening) return 'status-icon listening'
  return 'status-icon idle'
})

const connectionIcon = computed(() => {
  return sessionStore.isConnected ? Connection : Close
})

const connectionIconClass = computed(() => {
  return sessionStore.isConnected ? 'connection-icon connected' : 'connection-icon disconnected'
})

// 方法
async function toggleListening() {
  if (sessionStore.isListening) {
    await sessionStore.stopListening()
  } else {
    await sessionStore.startListening()
  }
}

async function sendTextMessage() {
  if (!inputText.value.trim()) return
  
  await sessionStore.sendTextMessage(inputText.value)
  inputText.value = ''
}

function clearResponse() {
  sessionStore.responseText = ''
  sessionStore.responseAudio = null
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString()
}
</script>

<style scoped>
.main-window {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.status-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-weight: 500;
}

.status-icon {
  font-size: 18px;
  transition: all 0.3s ease;
}

.status-icon.listening {
  color: #67c23a;
  animation: pulse 1.5s infinite;
}

.status-icon.processing {
  color: #409eff;
  animation: spin 1s linear infinite;
}

.status-icon.idle {
  color: #909399;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 14px;
}

.connection-icon.connected {
  color: #67c23a;
}

.connection-icon.disconnected {
  color: #f56c6c;
}

.main-content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.control-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-card,
.text-input-card,
.response-card,
.history-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #303133;
}

.voice-control {
  text-align: center;
  padding: 20px 0;
}

.voice-visualizer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  margin-bottom: 20px;
  height: 60px;
}

.voice-visualizer .wave {
  width: 4px;
  height: 20px;
  background: #e4e7ed;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.voice-visualizer.active .wave {
  background: #409eff;
  animation: wave 1.5s ease-in-out infinite;
}

.voice-visualizer.active .wave:nth-child(2) {
  animation-delay: 0.1s;
}

.voice-visualizer.active .wave:nth-child(3) {
  animation-delay: 0.2s;
}

.voice-visualizer.active .wave:nth-child(4) {
  animation-delay: 0.3s;
}

.voice-visualizer.active .wave:nth-child(5) {
  animation-delay: 0.4s;
}

.voice-hint {
  color: #606266;
  font-size: 14px;
  margin: 0;
}

.text-input-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.send-button {
  align-self: flex-end;
}

.response-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.response-content {
  min-height: 200px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.response-text {
  color: #303133;
  line-height: 1.6;
  white-space: pre-wrap;
}

.response-placeholder {
  color: #909399;
  font-style: italic;
  text-align: center;
  padding: 40px 0;
}

.error-alert {
  margin-top: 0;
}

.history-section {
  padding: 0 20px 20px;
  max-height: 300px;
}

.history-list {
  max-height: 200px;
  overflow-y: auto;
}

.history-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  border-left: 4px solid #e4e7ed;
  background: #f8f9fa;
}

.history-item.success {
  border-left-color: #67c23a;
}

.history-item.error {
  border-left-color: #f56c6c;
}

.history-time {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.history-input,
.history-output {
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 4px;
}

.history-input strong {
  color: #409eff;
}

.history-output strong {
  color: #67c23a;
}

.empty-history {
  text-align: center;
  color: #909399;
  padding: 40px 0;
  font-style: italic;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes wave {
  0%, 100% {
    height: 20px;
  }
  50% {
    height: 40px;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .status-bar {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
</style>



