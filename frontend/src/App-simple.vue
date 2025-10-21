<template>
  <div id="app">
    <h1>🎯 Echo Command 系统</h1>
    <div class="status">
      <p>连接状态: {{ isConnected ? '已连接' : '未连接' }}</p>
      <p>状态: {{ statusText }}</p>
    </div>
    
    <div class="controls">
      <button @click="testConnection" :disabled="isProcessing">
        {{ isProcessing ? '处理中...' : '测试连接' }}
      </button>
      
      <div class="input-area">
        <textarea 
          v-model="inputText" 
          placeholder="输入测试文本..."
          rows="3"
        ></textarea>
        <button @click="sendMessage" :disabled="!inputText.trim() || isProcessing">
          发送
        </button>
      </div>
    </div>
    
    <div v-if="response" class="response">
      <h3>AI响应:</h3>
      <pre>{{ response }}</pre>
    </div>
    
    <div v-if="error" class="error">
      <h3>错误:</h3>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const isConnected = ref(false)
const isProcessing = ref(false)
const inputText = ref('你好')
const response = ref('')
const error = ref('')

const statusText = computed(() => {
  if (isProcessing.value) return '处理中...'
  if (isConnected.value) return '已连接'
  return '未连接'
})

async function testConnection() {
  try {
    isProcessing.value = true
    error.value = ''
    
    const res = await fetch('http://127.0.0.1:8000/health')
    if (res.ok) {
      const data = await res.json()
      isConnected.value = true
      response.value = `连接成功: ${JSON.stringify(data, null, 2)}`
    } else {
      throw new Error(`HTTP ${res.status}`)
    }
  } catch (err) {
    error.value = `连接失败: ${err.message}`
    isConnected.value = false
  } finally {
    isProcessing.value = false
  }
}

async function sendMessage() {
  if (!inputText.value.trim()) return
  
  try {
    isProcessing.value = true
    error.value = ''
    
    const res = await fetch('http://127.0.0.1:8000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: inputText.value })
    })
    
    if (res.ok) {
      const data = await res.json()
      response.value = JSON.stringify(data, null, 2)
    } else {
      throw new Error(`HTTP ${res.status}`)
    }
  } catch (err) {
    error.value = `发送失败: ${err.message}`
  } finally {
    isProcessing.value = false
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-height: 100vh;
}

.status {
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
}

.controls {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
}

.input-area {
  margin-top: 15px;
}

textarea {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  margin: 10px 0;
  font-family: inherit;
}

button {
  background: #409eff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin: 5px;
}

button:hover:not(:disabled) {
  background: #66b1ff;
}

button:disabled {
  background: #c0c4cc;
  cursor: not-allowed;
}

.response, .error {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
}

.error {
  background: rgba(244, 67, 54, 0.2);
  color: #ff5252;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
