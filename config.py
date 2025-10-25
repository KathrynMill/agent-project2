#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - 您提供的API Key
"""

# 您提供的API Key
# 注意：如果这个Key无效，请检查是哪个服务商的API
LLM_CONFIG = {
    "provider": "custom",
    "api_key": "sk-ca1afda060bc12b11cdbc0e7d34a4e1f741325f6685430ceef06f4596eaf90aa",
    "base_url": "https://api.siliconflow.cn/v1",  # 尝试硅基流动
    "model": "deepseek-ai/DeepSeek-V2.5"
}

# 如果上面不行，您可以尝试其他base_url：
# "base_url": "https://api.deepseek.com/v1"
# "base_url": "https://api.openai.com/v1"
# "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8090
ENABLE_DEMO_FALLBACK = True

