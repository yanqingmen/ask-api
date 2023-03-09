# -*- coding：utf-8 -*-
"""
askapi inspect
"""
import inspect
from ask_api.config.askapi_config import MAX_FUNC_LEN


def get_func_name(func):
    """
    get function name
    """
    return func.__name__


def get_func_desc(func):
    """
    get function desc
    """
    return inspect.getdoc(func)


def get_func_source(func):
    """
    get function source
    """
    source = inspect.getsource(func)
    # 超过 MAX_FUNC_LEN 个字符时，需要进行截断，保留前后各 MAX_FUNC_LEN/2 个字符
    if len(source) > MAX_FUNC_LEN:
        source = source[:int(MAX_FUNC_LEN/2)] + "\n...\n" + source[-int(MAX_FUNC_LEN/2):]
    return source
