#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统控制器 - 执行实际的系统操作
负责：打开网站、播放音乐、文件操作、系统控制等
"""

import os
import subprocess
import webbrowser
import json
from typing import Dict, Any
from datetime import datetime


class SystemController:
    """系统控制器类"""
    
    def __init__(self):
        """初始化系统控制器"""
        self.music_player = None
        self.base_output_dir = os.path.expanduser("~/echo-command/output")
        
        # 确保输出目录存在
        os.makedirs(self.base_output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.base_output_dir, "articles"), exist_ok=True)
        os.makedirs(os.path.join(self.base_output_dir, "code"), exist_ok=True)
        os.makedirs(os.path.join(self.base_output_dir, "files"), exist_ok=True)
    
    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行动作的统一入口
        
        参数:
            action: 动作类型
            parameters: 动作参数
        
        返回:
            执行结果
        """
        print(f"\n🔧 执行动作: {action}")
        print(f"📦 参数: {json.dumps(parameters, ensure_ascii=False)}")
        
        # 根据动作类型分发到具体方法
        action_map = {
            "open_website": self.open_website,
            "play_music": self.play_music,
            "write_article": self.write_article,
            "generate_code": self.generate_code,
            "web_search": self.web_search,
            "file_operation": self.file_operation,
            "system_control": self.system_control,
            "general_response": self.general_response
        }
        
        handler = action_map.get(action)
        if handler:
            return handler(parameters)
        else:
            return {
                "success": False,
                "message": f"未知的动作类型: {action}"
            }
    
    def open_website(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        打开网站
        
        参数:
            url: 网站URL
            target_name或target: 网站名称
        """
        url = parameters.get("url", "")
        target_name = parameters.get("target_name") or parameters.get("target", "网站")
        
        if not url:
                return {
                "success": False,
                "message": "未提供URL"
            }
        
        try:
            # 使用webbrowser模块打开网站
            webbrowser.open(url)
            
                return {
                    "success": True,
                "action": "open_website",
                "message": f"已为您打开{target_name}",
                "url": url,
                "target": target_name
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"打开网站失败: {str(e)}"
            }
    
    def play_music(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        播放音乐
        
        参数:
            song_name: 歌曲名称
            artist: 歌手名称
        """
        song_name = parameters.get("song_name", "")
        artist = parameters.get("artist", "")
        
        # 构建搜索URL（使用网易云音乐搜索）
        search_query = f"{artist} {song_name}".strip()
        music_url = f"https://music.163.com/#/search/m/?s={search_query}"
        
        try:
            # 打开音乐搜索页面
            webbrowser.open(music_url)
            
            message = f"正在为您播放"
            if artist:
                message += f"{artist}的"
            if song_name and song_name != "未指定":
                message += f"《{song_name}》"
            else:
                message += "音乐"
            
                return {
                    "success": True,
                "action": "play_music",
                "message": message,
                "song": song_name,
                "artist": artist,
                "search_url": music_url
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"播放音乐失败: {str(e)}"
            }
    
    def write_article(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        写文章
        
        参数:
            topic: 文章主题
            length: 文章长度
        """
        topic = parameters.get("topic", "未指定主题")
        length = parameters.get("length", "medium")
        
        # 生成文章内容（这里使用示例内容，实际应该调用LLM生成）
        article_content = self._generate_article_content(topic, length)
            
            # 保存文章到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"article_{timestamp}.txt"
        filepath = os.path.join(self.base_output_dir, "articles", filename)
            
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"主题: {topic}\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(article_content)
            
            return {
                "success": True,
                "action": "write_article",
                "message": f"文章已生成并保存到: {filepath}",
                "topic": topic,
                "filepath": filepath,
                "content": article_content[:200] + "..." if len(article_content) > 200 else article_content
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"写文章失败: {str(e)}"
            }
    
    def _generate_article_content(self, topic: str, length: str) -> str:
        """
        生成文章内容（示例）
        实际应该调用LLM API生成
        """
        return f"""关于{topic}的文章

{topic}是一个重要而有趣的话题。在当今社会，{topic}已经成为人们关注的焦点之一。

首先，让我们来了解一下{topic}的基本概念。{topic}涉及多个方面，包括理论基础、实践应用以及未来发展趋势。

其次，{topic}在现实生活中有着广泛的应用。无论是在工作中还是在日常生活中，{topic}都能为我们带来便利和启发。

最后，展望未来，{topic}还有很大的发展空间。随着技术的进步和认知的深入，{topic}必将为我们的生活带来更多的可能性。

总之，{topic}是一个值得我们深入研究和持续关注的重要领域。

（注：这是一个示例文章，实际应该由LLM生成更详细和专业的内容）"""
    
    def generate_code(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成代码
        
        参数:
            requirements: 代码需求描述
            language: 编程语言
        """
        requirements = parameters.get("requirements", "")
        language = parameters.get("language", "python")
        
        # 生成代码（这里使用示例代码，实际应该调用LLM生成）
        code_content = self._generate_code_content(requirements, language)
        
        # 保存代码到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = self._get_file_extension(language)
        filename = f"code_{timestamp}.{extension}"
        filepath = os.path.join(self.base_output_dir, "code", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 需求: {requirements}\n")
                f.write(f"# 语言: {language}\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(code_content)
            
            return {
                "success": True,
                "action": "generate_code",
                "message": f"代码已生成并保存到: {filepath}",
                "language": language,
                "filepath": filepath,
                "code": code_content
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"生成代码失败: {str(e)}"
            }
    
    def _generate_code_content(self, requirements: str, language: str) -> str:
        """
        生成代码内容（示例）
        实际应该调用LLM API生成
        """
        if language.lower() == "python":
            return f"""def main():
    \"\"\"
    {requirements}
    \"\"\"
    print("Hello, World!")
    # TODO: 实现具体功能
    pass

if __name__ == "__main__":
    main()
"""
        else:
            return f"// {requirements}\n// TODO: 实现代码\n"
    
    def _get_file_extension(self, language: str) -> str:
        """获取编程语言的文件扩展名"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "c++": "cpp",
            "c": "c",
            "go": "go",
            "rust": "rs"
        }
        return extensions.get(language.lower(), "txt")
    
    def web_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        网络搜索
        
        参数:
            query: 搜索关键词
        """
        query = parameters.get("query", "")
        
        if not query:
            return {
                "success": False,
                "message": "未提供搜索关键词"
            }
        
        # 使用百度搜索
        search_url = f"https://www.baidu.com/s?wd={query}"
        
        try:
            webbrowser.open(search_url)
            
            return {
                "success": True,
                "action": "web_search",
                "message": f"正在为您搜索: {query}",
                "query": query,
                "search_url": search_url
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"搜索失败: {str(e)}"
            }
    
    def file_operation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        文件操作
        
        参数:
            operation: 操作类型 (create/read/write/delete)
            file_path: 文件路径
            content: 文件内容
        """
        operation = parameters.get("operation", "")
        file_path = parameters.get("file_path", "")
        content = parameters.get("content", "")
        
        try:
            if operation == "create" or operation == "write":
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {
                    "success": True,
                    "action": "file_operation",
                    "message": f"文件已保存: {file_path}",
                    "operation": operation,
                    "file_path": file_path
                }
            
            elif operation == "read":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "success": True,
                    "action": "file_operation",
                    "message": "文件读取成功",
                    "operation": operation,
                    "file_path": file_path,
                    "content": content
                }
            
            else:
                return {
                    "success": False,
                    "message": f"不支持的操作: {operation}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"文件操作失败: {str(e)}"
            }
    
    def system_control(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        系统控制
        
        参数:
            action: 控制动作
            value: 控制值
        """
        action = parameters.get("action", "")
        
            return {
                "success": True,
            "action": "system_control",
            "message": f"系统控制功能开发中: {action}"
        }
    
    def general_response(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        一般响应
        """
        message = parameters.get("message", "我明白了")
        
            return {
            "success": True,
            "action": "general_response",
            "message": message
        }


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("系统控制器测试")
    print("=" * 60)
    
    controller = SystemController()
    
    # 测试打开网站
    print("\n【测试1: 打开网站】")
    result = controller.execute_action("open_website", {
        "url": "https://github.com",
        "target_name": "GitHub"
    })
    print(f"结果: {result}")
    
    # 测试写文章
    print("\n【测试2: 写文章】")
    result = controller.execute_action("write_article", {
        "topic": "人工智能",
        "length": "medium"
    })
    print(f"结果: {result.get('message')}")
