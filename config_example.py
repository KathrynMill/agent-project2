#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件示例
复制此文件为 config.py 并填入您的真实API信息
"""

# ============================================================
# LLM配置（大语言模型）
# ============================================================

# 选项1: 硅基流动 (推荐，免费额度充足)
LLM_CONFIG = {
    "provider": "siliconflow",
    "api_key": "sk-your-api-key-here",
    "base_url": "https://api.siliconflow.cn/v1",
    "model": "deepseek-ai/DeepSeek-V2.5"
}

# 选项2: DeepSeek
# LLM_CONFIG = {
#     "provider": "deepseek",
#     "api_key": "sk-your-api-key-here",
#     "base_url": "https://api.deepseek.com/v1",
#     "model": "deepseek-chat"
# }

# 选项3: 百度文心一言
# LLM_CONFIG = {
#     "provider": "baidu",
#     "api_key": "your-api-key",
#     "secret_key": "your-secret-key"
# }

# 选项4: 通义千问
# LLM_CONFIG = {
#     "provider": "qianwen",
#     "api_key": "sk-your-api-key-here",
#     "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
#     "model": "qwen-turbo"
# }

# ============================================================
# 其他配置
# ============================================================

# 服务器配置
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8090

# 是否启用演示模式（如果API配置失败，自动回退到演示模式）
ENABLE_DEMO_FALLBACK = True

