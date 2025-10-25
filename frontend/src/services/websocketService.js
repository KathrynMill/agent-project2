/**
 * WebSocket服务
 */
export class WebSocketService {
  constructor() {
    this.ws = null
    this.url = 'ws://127.0.0.1:8000/ws'
    this.reconnectInterval = 5000
    this.maxReconnectAttempts = 5
    this.reconnectAttempts = 0
    this.messageHandlers = []
    this.errorHandlers = []
    this.closeHandlers = []
  }
  
  async connect() {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url)
        
        this.ws.onopen = () => {
          console.log('WebSocket连接已建立')
          this.reconnectAttempts = 0
          resolve()
        }
        
        this.ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data)
            this.messageHandlers.forEach(handler => handler(message))
          } catch (error) {
            console.error('解析WebSocket消息失败:', error)
          }
        }
        
        this.ws.onerror = (error) => {
          console.error('WebSocket错误:', error)
          this.errorHandlers.forEach(handler => handler(error))
          reject(error)
        }
        
        this.ws.onclose = (event) => {
          console.log('WebSocket连接关闭:', event.code, event.reason)
          this.closeHandlers.forEach(handler => handler(event))
          
          // 自动重连
          if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++
            console.log(`尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`)
            setTimeout(() => {
              this.connect().catch(console.error)
            }, this.reconnectInterval)
          }
        }
        
      } catch (error) {
        reject(error)
      }
    })
  }
  
  async disconnect() {
    if (this.ws) {
      this.ws.close(1000, '正常关闭')
      this.ws = null
    }
  }
  
  async send(message) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket未连接')
    }
    
    this.ws.send(JSON.stringify(message))
  }
  
  onMessage(handler) {
    this.messageHandlers.push(handler)
  }
  
  onError(handler) {
    this.errorHandlers.push(handler)
  }
  
  onClose(handler) {
    this.closeHandlers.push(handler)
  }
  
  removeMessageHandler(handler) {
    const index = this.messageHandlers.indexOf(handler)
    if (index > -1) {
      this.messageHandlers.splice(index, 1)
    }
  }
  
  removeErrorHandler(handler) {
    const index = this.errorHandlers.indexOf(handler)
    if (index > -1) {
      this.errorHandlers.splice(index, 1)
    }
  }
  
  removeCloseHandler(handler) {
    const index = this.closeHandlers.indexOf(handler)
    if (index > -1) {
      this.closeHandlers.splice(index, 1)
    }
  }
}





