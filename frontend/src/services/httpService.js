/**
 * HTTP服务 - 替代WebSocket进行API通信
 */
export class HttpService {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:8000'
    this.isConnected = false
  }
  
  async connect() {
    try {
      // 检查服务器健康状态
      const response = await fetch(`${this.baseUrl}/health`)
      if (response.ok) {
        this.isConnected = true
        console.log('HTTP服务连接成功')
        return true
      } else {
        throw new Error('服务器响应异常')
      }
    } catch (error) {
      console.error('HTTP服务连接失败:', error)
      this.isConnected = false
      throw error
    }
  }
  
  async disconnect() {
    this.isConnected = false
    console.log('HTTP服务已断开')
  }
  
  async sendMessage(message) {
    if (!this.isConnected) {
      throw new Error('HTTP服务未连接')
    }
    
    try {
      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(message)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
      }
      
      const data = await response.json()
      return data
      
    } catch (error) {
      console.error('发送消息失败:', error)
      throw error
    }
  }
  
  async sendTextMessage(text) {
    return await this.sendMessage({
      type: 'text',
      text: text
    })
  }
  
  // 为了兼容WebSocket接口，添加这些方法
  onMessage(handler) {
    // HTTP服务不需要消息监听
    console.log('HTTP服务不支持消息监听')
  }
  
  onError(handler) {
    // HTTP服务错误处理在sendMessage中
    console.log('HTTP服务错误处理已集成')
  }
  
  onClose(handler) {
    // HTTP服务不需要连接关闭处理
    console.log('HTTP服务不需要连接关闭处理')
  }
}


