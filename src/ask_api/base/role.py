# -*- coding: utf-8 -*-
"""
askapi role
"""
from ask_api.llm.base import LLMBase
from ask_api.util.askapi_log import logging
from ask_api.util.askapi_asyn import run_async_task, wait_task
from ask_api.util.askapi_util import get_json_from_text
from .session import Message, Session
import json


class Role(object):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def answer(self, message: str, mode: str = 'free', session: Session = None) -> Message:
        raise NotImplementedError("answer() is not implemented")

    def ask(self) -> str:
        raise NotImplementedError("ask() is not implemented")


class FunctionRole(Role):
    """
    函数角色
    Args:
        Role (_type_): _description_
    """

    def __init__(self, llm: LLMBase, func, name: str = None) -> None:
        if name:
            super().__init__(name)
        else:
            super().__init__(func.__name__)
        self.func = func
        self.llm = llm
        self.desc = None

    def answer(self, message: Message, mode: str = 'free', session: Session = None) -> Message:
        """
        Args:
            message (Message): message info
            mode (str, optional): _description_. Defaults to 'free'.
            session (Session, optional): _description_. Defaults to None.
        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_

        """
        if mode == "desc":
            return self.ask()
        elif mode == "execute":
            return self.execute(message, session)
        elif mode == "free":
            answer = self.llm.free_answer(self.func, message)
            return Message(role=self, text=answer)
        else:
            raise ValueError("mode must be one of desc, execute, free")

    def execute(self, message: Message, session: Session = None) -> Message:
        """
        执行任务
        Args:
            message (str): a str message
            session (Session, optional): _description_. Defaults to None.
        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        param_json = self.llm.execute_param(self.func, message)
        try:
            param_dic = get_json_from_text(param_json)
        except Exception as e:
            return Message(role=self, text=param_json)

        # 异步执行函数
        async def execute():
            try:
                ret = self.func(**param_dic)
                answer = self.llm.return_value(self.func, ret)
                async_message = Message(role=self, text=answer)
            except Exception as ex:
                ex_desc = self.llm.exception(self.func, str(ex))
                ex_message = self.llm.exception_message().format(message=ex_desc)
                async_message = Message(role=self, text=ex_message)
            if session:
                session.add_message(async_message)
            return async_message

        task = run_async_task(execute())
        execute_message = self.llm.execute_message()
        return Message(role=self, text=execute_message, task=task)

    def ask(self) -> Message:
        """
        Returns:
            str: _description_
        """
        if not self.desc:
            self.desc = self.llm.desc(self.func)
        text = self.desc
        return Message(role=self, text=text)


class UserRole(Role):
    """
    用户角色（虚拟角色，只是用于占位，不进行任何调用）
    Args:
        Role (_type_): _description_
    """

    def __init__(self, name) -> None:
        super().__init__(name)

    def answer(self, message: str, mode: str = 'free', session: Session = None) -> Message:
        """
        Args:
            message (str): _description_
            mode (str, optional): _description_. Defaults to 'free'.
            session (Session, optional): _description_. Defaults to None.
        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        raise ValueError("user role can not answer")

    def ask(self) -> str:
        """
        Returns:
            str: _description_
        """
        raise ValueError("user role can not ask")


class CLIUserRole(UserRole):
    """
    命令行用户角色(用于命令行交互式提问)
    Args:
        UserRole (_type_): _description_
    """

    def __init__(self, name) -> None:
        super().__init__(name)

    def answer(self, message: str, mode: str = 'free', session: Session = None):
        """
        Args:
            message (str): _description_
            mode (str, optional): _description_. Defaults to 'free'
            session (Session, optional): _description_. Defaults to None.
        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        # 从命令行获取输入
        answer = input(self.name + ":")
        return answer

    def ask(self) -> str:
        """
        Returns:
            str: _description_
        """
        message = input(self.name + ":")
        return message
