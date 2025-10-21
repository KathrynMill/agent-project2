import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { HttpService } from '../services/httpService'
import { AudioService } from '../services/audioService'

export const useSessionStore = defineStore('session', () => {
  // 状态
  const isConnected = ref(false)
  const isListening = ref(false)
  const isProcessing = ref(false)
  const sessionId = ref(null)
  const currentText = ref('')
  const responseText = ref('')
  const responseAudio = ref(null)
  const errorMessage = ref('')
  const commandHistory = ref([])
  
  // 服务实例
  const httpService = new HttpService()
  const audioService = new AudioService()
  
  // 计算属性
  const statusText = computed(() => {
    if (isProcessing.value) return '处理中...'
    if (isListening.value) return '正在聆听...'
    if (isConnected.value) return '已连接'
    return '未连接'
  })
  
  const canStartListening = computed(() => {
    return isConnected.value && !isListening.value && !isProcessing.value
  })
  
  // 方法
  async function initialize() {
    try {
      await connect()
      await audioService.initialize()
    } catch (error) {
      console.error('初始化失败:', error)
      errorMessage.value = '初始化失败: ' + error.message
    }
  }
  
  async function connect() {
    try {
      await httpService.connect()
      isConnected.value = true
      errorMessage.value = ''
      
    } catch (error) {
      console.error('连接失败:', error)
      errorMessage.value = '连接失败: ' + error.message
      throw error
    }
  }
  
  async function disconnect() {
    try {
      await httpService.disconnect()
      isConnected.value = false
      sessionId.value = null
    } catch (error) {
      console.error('断开连接失败:', error)
    }
  }
  
  async function startListening() {
    if (!canStartListening.value) return
    
    try {
      isListening.value = true
      errorMessage.value = ''
      
      // 开始录音
      await audioService.startRecording()
      
      // 监听音频数据
      audioService.onAudioData((audioData) => {
        sendAudioMessage(audioData)
      })
      
    } catch (error) {
      console.error('开始聆听失败:', error)
      errorMessage.value = '开始聆听失败: ' + error.message
      isListening.value = false
    }
  }
  
  async function stopListening() {
    try {
      isListening.value = false
      await audioService.stopRecording()
    } catch (error) {
      console.error('停止聆听失败:', error)
      errorMessage.value = '停止聆听失败: ' + error.message
    }
  }
  
  async function sendTextMessage(text) {
    if (!isConnected.value || !text.trim()) return
    
    try {
      isProcessing.value = true
      currentText.value = text
      
      const response = await httpService.sendTextMessage(text)
      handleMessage(response)
      
    } catch (error) {
      console.error('发送文本消息失败:', error)
      errorMessage.value = '发送文本消息失败: ' + error.message
      isProcessing.value = false
    }
  }
  
  async function sendAudioMessage(audioData) {
    if (!isConnected.value) return
    
    try {
      const message = {
        type: 'audio',
        audio_data: audioData,
        sample_rate: 16000,
        session_id: sessionId.value
      }
      
      await wsService.send(message)
      
    } catch (error) {
      console.error('发送音频消息失败:', error)
      errorMessage.value = '发送音频消息失败: ' + error.message
    }
  }
  
  function handleMessage(message) {
    console.log('收到消息:', message)
    
    if (message.type === 'response') {
      isProcessing.value = false
      isListening.value = false
      
      responseText.value = message.message
      
      if (message.audio_response) {
        responseAudio.value = message.audio_response
        playResponseAudio()
      }
      
      // 添加到历史记录
      commandHistory.value.unshift({
        id: Date.now(),
        timestamp: new Date(),
        input: currentText.value,
        output: message.message,
        success: message.success,
        data: message.data
      })
      
      // 限制历史记录数量
      if (commandHistory.value.length > 100) {
        commandHistory.value = commandHistory.value.slice(0, 100)
      }
      
    } else if (message.type === 'error') {
      isProcessing.value = false
      isListening.value = false
      errorMessage.value = message.error_message
    }
  }
  
  function handleError(error) {
    console.error('WebSocket错误:', error)
    errorMessage.value = '连接错误: ' + error.message
    isConnected.value = false
  }
  
  function handleClose() {
    console.log('WebSocket连接关闭')
    isConnected.value = false
    isListening.value = false
    isProcessing.value = false
  }
  
  async function playResponseAudio() {
    if (!responseAudio.value) return
    
    try {
      // 将十六进制字符串转换为音频数据
      const audioData = new Uint8Array(
        responseAudio.value.match(/.{2}/g).map(byte => parseInt(byte, 16))
      )
      
      await audioService.playAudio(audioData)
      
    } catch (error) {
      console.error('播放音频失败:', error)
    }
  }
  
  function clearError() {
    errorMessage.value = ''
  }
  
  function clearHistory() {
    commandHistory.value = []
  }
  
  return {
    // 状态
    isConnected,
    isListening,
    isProcessing,
    sessionId,
    currentText,
    responseText,
    responseAudio,
    errorMessage,
    commandHistory,
    
    // 计算属性
    statusText,
    canStartListening,
    
    // 方法
    initialize,
    connect,
    disconnect,
    startListening,
    stopListening,
    sendTextMessage,
    clearError,
    clearHistory
  }
})



