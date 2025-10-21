#!/usr/bin/env python3
"""
系统控制器 - 实现真正的电脑控制功能
"""

import os
import subprocess
import platform
import json
import time
from typing import Dict, Any, Optional

class SystemController:
    """系统控制器 - 控制电脑的各种功能"""
    
    def __init__(self):
        self.os_type = platform.system().lower()
        print(f"🖥️  检测到操作系统: {self.os_type}")
    
    def play_music(self, query: str = "") -> Dict[str, Any]:
        """播放音乐"""
        try:
            if self.os_type == "linux":
                # Linux系统 - 尝试打开音乐播放器
                music_apps = ["vlc", "rhythmbox", "audacious", "amarok", "banshee"]
                for app in music_apps:
                    try:
                        subprocess.Popen([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return {
                            "success": True,
                            "message": f"正在打开音乐播放器 {app}...",
                            "action": "play_music",
                            "app": app
                        }
                    except FileNotFoundError:
                        continue
                
                # 如果没有找到音乐播放器，尝试播放系统声音
                subprocess.Popen(["paplay", "/usr/share/sounds/alsa/Front_Left.wav"], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {
                    "success": True,
                    "message": "正在播放系统声音...",
                    "action": "play_music",
                    "app": "system_sound"
                }
            
            elif self.os_type == "windows":
                # Windows系统
                subprocess.Popen(["start", "wmplayer"], shell=True)
                return {
                    "success": True,
                    "message": "正在打开Windows Media Player...",
                    "action": "play_music",
                    "app": "wmplayer"
                }
            
            elif self.os_type == "darwin":  # macOS
                subprocess.Popen(["open", "-a", "Music"])
                return {
                    "success": True,
                    "message": "正在打开Apple Music...",
                    "action": "play_music",
                    "app": "music"
                }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"播放音乐失败: {str(e)}",
                "action": "play_music",
                "error": str(e)
            }
    
    def open_browser(self, url: str = "https://www.baidu.com") -> Dict[str, Any]:
        """打开浏览器"""
        try:
            if self.os_type == "linux":
                browsers = ["firefox", "google-chrome", "chromium-browser", "opera", "konqueror"]
                for browser in browsers:
                    try:
                        subprocess.Popen([browser, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        return {
                            "success": True,
                            "message": f"正在打开浏览器 {browser}...",
                            "action": "open_browser",
                            "browser": browser,
                            "url": url
                        }
                    except FileNotFoundError:
                        continue
                
                # 使用xdg-open作为备选
                subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {
                    "success": True,
                    "message": f"正在打开默认浏览器访问 {url}...",
                    "action": "open_browser",
                    "browser": "default",
                    "url": url
                }
            
            elif self.os_type == "windows":
                subprocess.Popen(["start", url], shell=True)
                return {
                    "success": True,
                    "message": f"正在打开浏览器访问 {url}...",
                    "action": "open_browser",
                    "browser": "default",
                    "url": url
                }
            
            elif self.os_type == "darwin":  # macOS
                subprocess.Popen(["open", url])
                return {
                    "success": True,
                    "message": f"正在打开Safari访问 {url}...",
                    "action": "open_browser",
                    "browser": "safari",
                    "url": url
                }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"打开浏览器失败: {str(e)}",
                "action": "open_browser",
                "error": str(e)
            }
    
    def adjust_volume(self, level: int = 50) -> Dict[str, Any]:
        """调节音量"""
        try:
            if self.os_type == "linux":
                # 使用pactl调节音量
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], 
                              check=True, capture_output=True)
                return {
                    "success": True,
                    "message": f"音量已调节到 {level}%",
                    "action": "adjust_volume",
                    "level": level
                }
            elif self.os_type == "windows":
                # Windows音量控制
                subprocess.run(["powershell", "-Command", f"(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], 
                              check=True)
                return {
                    "success": True,
                    "message": f"正在调节音量...",
                    "action": "adjust_volume",
                    "level": level
                }
            elif self.os_type == "darwin":  # macOS
                subprocess.run(["osascript", "-e", f"set volume output volume {level}"], 
                              check=True)
                return {
                    "success": True,
                    "message": f"音量已调节到 {level}%",
                    "action": "adjust_volume",
                    "level": level
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"调节音量失败: {str(e)}",
                "action": "adjust_volume",
                "error": str(e)
            }
    
    def write_article(self, topic: str, content: str = "") -> Dict[str, Any]:
        """写文章功能"""
        try:
            # 创建文章内容
            article_content = f"""
# {topic}

## 文章摘要
这是一篇关于"{topic}"的文章，由Echo Command AI助手生成。

## 正文内容
{content if content else f"关于{topic}的详细内容将在这里展开。这是一个由AI生成的示例文章，展示了Echo Command系统的文本生成能力。"}

## 结论
本文讨论了{topic}的相关内容，展示了AI助手在文本生成方面的能力。

---
*本文由Echo Command AI助手生成于 {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            # 保存文章到文件
            filename = f"article_{int(time.time())}.md"
            filepath = os.path.join(os.getcwd(), filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(article_content)
            
            # 尝试打开文件
            if self.os_type == "linux":
                subprocess.Popen(["xdg-open", filepath])
            elif self.os_type == "windows":
                subprocess.Popen(["start", filepath], shell=True)
            elif self.os_type == "darwin":
                subprocess.Popen(["open", filepath])
            
            return {
                "success": True,
                "message": f"文章已生成并保存为 {filename}",
                "action": "write_article",
                "filename": filename,
                "filepath": filepath,
                "content": article_content[:200] + "..." if len(article_content) > 200 else article_content
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"写文章失败: {str(e)}",
                "action": "write_article",
                "error": str(e)
            }
    
    def open_application(self, app_name: str) -> Dict[str, Any]:
        """打开应用程序"""
        try:
            if self.os_type == "linux":
                # Linux应用启动
                subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {
                    "success": True,
                    "message": f"正在打开 {app_name}...",
                    "action": "open_application",
                    "app": app_name
                }
            elif self.os_type == "windows":
                subprocess.Popen(["start", app_name], shell=True)
                return {
                    "success": True,
                    "message": f"正在打开 {app_name}...",
                    "action": "open_application",
                    "app": app_name
                }
            elif self.os_type == "darwin":
                subprocess.Popen(["open", "-a", app_name])
                return {
                    "success": True,
                    "message": f"正在打开 {app_name}...",
                    "action": "open_application",
                    "app": app_name
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"打开应用失败: {str(e)}",
                "action": "open_application",
                "error": str(e)
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        try:
            return {
                "success": True,
                "message": "系统信息获取成功",
                "action": "get_system_info",
                "data": {
                    "os": self.os_type,
                    "platform": platform.platform(),
                    "python_version": platform.python_version(),
                    "current_directory": os.getcwd(),
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"获取系统信息失败: {str(e)}",
                "action": "get_system_info",
                "error": str(e)
            }

def test_system_controller():
    """测试系统控制器"""
    print("🎯 Echo Command - 系统控制器测试")
    print("=" * 50)
    
    controller = SystemController()
    
    # 测试各种功能
    tests = [
        ("获取系统信息", lambda: controller.get_system_info()),
        ("播放音乐", lambda: controller.play_music()),
        ("打开浏览器", lambda: controller.open_browser()),
        ("调节音量", lambda: controller.adjust_volume(70)),
        ("写文章", lambda: controller.write_article("AI技术发展", "AI技术正在快速发展...")),
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 测试: {test_name}")
        try:
            result = test_func()
            print(f"结果: {result['message']}")
            print(f"成功: {result['success']}")
        except Exception as e:
            print(f"错误: {str(e)}")
    
    print("\n✅ 系统控制器测试完成！")

if __name__ == "__main__":
    test_system_controller()
