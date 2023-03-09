# -*- coding: utf-8 -*-
"""
测试异步调用函数相关工具
"""

from ask_api.util.askapi_asyn import run_async_task, wait_task


def test_run_async_task():
    async def func():
        return 1

    task = run_async_task(func())
    assert wait_task(task) == 1
