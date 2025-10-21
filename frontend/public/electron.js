const { app, BrowserWindow, Tray, Menu, ipcMain, dialog } = require('electron')
const path = require('path')
const isDev = process.env.NODE_ENV === 'development'

let mainWindow
let tray
let isQuitting = false

function createWindow() {
  // 创建浏览器窗口
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    icon: path.join(__dirname, 'icon.png'),
    show: false, // 初始不显示窗口
    titleBarStyle: 'hiddenInset'
  })

  // 加载应用
  const startUrl = isDev 
    ? 'http://localhost:5173' 
    : `file://${path.join(__dirname, '../dist/index.html')}`
  
  mainWindow.loadURL(startUrl)

  // 当窗口准备好时显示
  mainWindow.once('ready-to-show', () => {
    if (isDev) {
      mainWindow.show()
    }
  })

  // 当窗口关闭时隐藏而不是退出
  mainWindow.on('close', (event) => {
    if (!isQuitting) {
      event.preventDefault()
      mainWindow.hide()
    }
  })

  // 开发环境下打开开发者工具
  if (isDev) {
    mainWindow.webContents.openDevTools()
  }
}

function createTray() {
  // 创建系统托盘
  const iconPath = path.join(__dirname, 'tray-icon.png')
  tray = new Tray(iconPath)
  
  const contextMenu = Menu.buildFromTemplate([
    {
      label: '显示主窗口',
      click: () => {
        mainWindow.show()
        mainWindow.focus()
      }
    },
    {
      label: '开始聆听',
      click: () => {
        mainWindow.webContents.send('start-listening')
      }
    },
    {
      label: '停止聆听',
      click: () => {
        mainWindow.webContents.send('stop-listening')
      }
    },
    { type: 'separator' },
    {
      label: '设置',
      click: () => {
        mainWindow.show()
        mainWindow.webContents.send('open-settings')
      }
    },
    { type: 'separator' },
    {
      label: '退出',
      click: () => {
        isQuitting = true
        app.quit()
      }
    }
  ])
  
  tray.setContextMenu(contextMenu)
  tray.setToolTip('Echo Command - 语音控制助手')
  
  // 双击托盘图标显示主窗口
  tray.on('double-click', () => {
    mainWindow.show()
    mainWindow.focus()
  })
}

// 当 Electron 完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(() => {
  createWindow()
  createTray()
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    } else {
      mainWindow.show()
    }
  })
})

// 当所有窗口关闭时退出应用
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// 应用即将退出时
app.on('before-quit', () => {
  isQuitting = true
})

// IPC 通信处理
ipcMain.handle('show-message-box', async (event, options) => {
  const result = await dialog.showMessageBox(mainWindow, options)
  return result
})

ipcMain.handle('show-save-dialog', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options)
  return result
})

ipcMain.handle('show-open-dialog', async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options)
  return result
})

// 处理应用协议
app.setAsDefaultProtocolClient('echo-command')

// 处理协议链接
app.on('open-url', (event, url) => {
  event.preventDefault()
  // 处理协议链接
  console.log('Received URL:', url)
})



