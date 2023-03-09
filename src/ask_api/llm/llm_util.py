# -*- coding: utf-8 -*-
"""
llm 工具函数
"""
from typing import Dict

from ask_api.util.askapi_log import logging
from ask_api.config.askapi_config import DEFAULT_LLM_MODEL, LANG
from ask_api.prompt.basic import ALL_BASIC_PROMPTS
from .base import LLMBase, LLMBuilder

LLM_BUILDERS = {}


def register_llm_builder(name: str):
    """
    注册 LLM builder
    :param name:
    :return:
    """
    def _register_llm_builder(cls: LLMBuilder) -> LLMBuilder:
        if name in LLM_BUILDERS:
            raise ValueError(f"Cannot register duplicate LLM builder ({name})")
        if not issubclass(cls.__class__, LLMBuilder):
            raise ValueError(f"LLM builder ({name}) must extend LLMBuilder")
        LLM_BUILDERS[name] = cls
        return cls

    return _register_llm_builder


def build_llm(name: str, prompt_config: Dict) -> LLMBase:
    """
    构建 LLM
    :param name:
    :param prompt_config:
    :return:
    """
    if name not in LLM_BUILDERS:
        raise ValueError(f"Unregistered LLM builder ({name})")
    return LLM_BUILDERS[name](prompt_config)


def list_llm() -> list:
    """
    获取所有的 LLM
    :return:
    """
    return list(LLM_BUILDERS.keys())


# 注册各个 LLM Builder
# 注册 OpenAIChatBuilder
try:
    from .openai import OpenAIChatBuilder
    register_llm_builder(OpenAIChatBuilder.builder_name())(OpenAIChatBuilder())
except ImportError:
    logging.warning("OpenAIChatBuilder is not available, please install openai package")
    pass
except Exception as e:
    logging.warning("OpenAIChatBuilder is not available, error: {}".format(e))
    pass


# 构造 Default LLM
def build_default_llm() -> LLMBase:
    """
    构造 Default LLM
    :return:
    """
    try:
        prompt_config = ALL_BASIC_PROMPTS[LANG]
    except KeyError:
        raise ValueError(f"Unsupported language ({LANG})")

    default_llm_name = DEFAULT_LLM_MODEL
    return build_llm(default_llm_name, prompt_config)

