# -*- coding: utf-8 -*-
"""
ask api 相关基础配置
"""
import os

# 语言配置，zh 为中文，en 为英文
LANG = "zh"

# llm模型阅读函数的最大长度
MAX_FUNC_LEN = 1024

# 是否为debug模型
ASK_API_DEBUG = False

# openai api key path
OPENAI_KEY_PATH = "config/open-ai.key"
OPENAI_KEY = None

# DEFAULT_LLM_MODEL
DEFAULT_LLM_MODEL = "openai_chat"
DEFAULT_OPENAI_CHAT_MODEL = "gpt-3.5-turbo"
