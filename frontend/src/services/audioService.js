/**
 * 音频服务
 */
export class AudioService {
  constructor() {
    this.mediaRecorder = null
    this.audioContext = null
    this.audioStream = null
    this.isRecording = false
    this.audioDataHandlers = []
  }
  
  async initialize() {
    try {
      // 获取麦克风权限
      this.audioStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        }
      })
      
      // 创建音频上下文
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 16000
      })
      
      console.log('音频服务初始化成功')
      
    } catch (error) {
      console.error('音频服务初始化失败:', error)
      throw error
    }
  }
  
  async startRecording() {
    if (this.isRecording) return
    
    try {
      if (!this.audioStream) {
        await this.initialize()
      }
      
      // 创建MediaRecorder
      this.mediaRecorder = new MediaRecorder(this.audioStream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      const audioChunks = []
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }
      
      this.mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        const audioData = await this.convertToWav(audioBlob)
        
        // 通知所有监听器
        this.audioDataHandlers.forEach(handler => handler(audioData))
      }
      
      // 开始录音
      this.mediaRecorder.start(100) // 每100ms收集一次数据
      this.isRecording = true
      
      console.log('开始录音')
      
    } catch (error) {
      console.error('开始录音失败:', error)
      throw error
    }
  }
  
  async stopRecording() {
    if (!this.isRecording || !this.mediaRecorder) return
    
    try {
      this.mediaRecorder.stop()
      this.isRecording = false
      
      console.log('停止录音')
      
    } catch (error) {
      console.error('停止录音失败:', error)
      throw error
    }
  }
  
  async convertToWav(audioBlob) {
    try {
      const arrayBuffer = await audioBlob.arrayBuffer()
      const audioContext = new (window.AudioContext || window.webkitAudioContext)()
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
      
      // 转换为WAV格式
      const wavData = this.audioBufferToWav(audioBuffer)
      
      // 转换为Base64字符串
      const base64 = this.arrayBufferToBase64(wavData)
      
      return base64
      
    } catch (error) {
      console.error('音频转换失败:', error)
      throw error
    }
  }
  
  audioBufferToWav(buffer) {
    const length = buffer.length
    const sampleRate = buffer.sampleRate
    const arrayBuffer = new ArrayBuffer(44 + length * 2)
    const view = new DataView(arrayBuffer)
    
    // WAV文件头
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i))
      }
    }
    
    writeString(0, 'RIFF')
    view.setUint32(4, 36 + length * 2, true)
    writeString(8, 'WAVE')
    writeString(12, 'fmt ')
    view.setUint32(16, 16, true)
    view.setUint16(20, 1, true)
    view.setUint16(22, 1, true)
    view.setUint32(24, sampleRate, true)
    view.setUint32(28, sampleRate * 2, true)
    view.setUint16(32, 2, true)
    view.setUint16(34, 16, true)
    writeString(36, 'data')
    view.setUint32(40, length * 2, true)
    
    // 写入音频数据
    const channelData = buffer.getChannelData(0)
    let offset = 44
    for (let i = 0; i < length; i++) {
      const sample = Math.max(-1, Math.min(1, channelData[i]))
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true)
      offset += 2
    }
    
    return arrayBuffer
  }
  
  arrayBufferToBase64(buffer) {
    let binary = ''
    const bytes = new Uint8Array(buffer)
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i])
    }
    return btoa(binary)
  }
  
  async playAudio(audioData) {
    try {
      // 将Uint8Array转换为ArrayBuffer
      const arrayBuffer = audioData.buffer.slice(audioData.byteOffset, audioData.byteOffset + audioData.byteLength)
      
      // 创建音频上下文
      const audioContext = new (window.AudioContext || window.webkitAudioContext)()
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
      
      // 创建音频源
      const source = audioContext.createBufferSource()
      source.buffer = audioBuffer
      source.connect(audioContext.destination)
      
      // 播放音频
      source.start()
      
      console.log('播放音频')
      
    } catch (error) {
      console.error('播放音频失败:', error)
      throw error
    }
  }
  
  onAudioData(handler) {
    this.audioDataHandlers.push(handler)
  }
  
  removeAudioDataHandler(handler) {
    const index = this.audioDataHandlers.indexOf(handler)
    if (index > -1) {
      this.audioDataHandlers.splice(index, 1)
    }
  }
  
  cleanup() {
    if (this.audioStream) {
      this.audioStream.getTracks().forEach(track => track.stop())
      this.audioStream = null
    }
    
    if (this.audioContext) {
      this.audioContext.close()
      this.audioContext = null
    }
    
    this.mediaRecorder = null
    this.isRecording = false
  }
}

