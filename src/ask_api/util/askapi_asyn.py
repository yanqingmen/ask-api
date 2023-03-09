# -*- coding: utf-8 -*-
"""
异步调用函数相关工具
"""
import nest_asyncio
nest_asyncio.apply()

import asyncio

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


def run_async_task(func):
    """
    异步调用函数
    """
    task = loop.create_task(func)
    return task


def close_loop():
    """
    关闭loop
    """
    loop.close()


def wait_task(task):
    """
    等待task执行完成
    """
    loop.run_until_complete(task)
    return task.result()
