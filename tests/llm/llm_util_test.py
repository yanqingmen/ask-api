# -*- coding: utf-8 -*-
"""
llm util test
"""
from ask_api.llm.base import LLMBase
from ask_api.config import askapi_config
from ask_api.llm.llm_util import build_default_llm


def split_text(text: str, sep: str = " ") -> list:
    """
    demo function
    """
    return text.split(sep)


def test_build_default_llm():
    llm = build_default_llm()
    assert issubclass(llm.__class__, LLMBase)


def test_lang():
    askapi_config.LANG = "zh"
    zh_llm = build_default_llm()
    print("zh_llm desc: ", zh_llm.desc(split_text))

    askapi_config.LANG = "en"
    en_llm = build_default_llm()
    print("en_llm desc: ", en_llm.desc(split_text))


