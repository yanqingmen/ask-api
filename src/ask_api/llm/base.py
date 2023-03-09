# -*- coding: utf-8 -*-
"""
llm 主要用于生成如下信息：
1. 函数的功能描述
2. 用户自然语言输入与函数参数的映射
3. 函数的返回值描述
4. 函数的异常信息描述
5. 与函数进行自由回答
"""
from abc import ABC, abstractmethod
from typing import Dict


class AskApiPrompt(ABC):
    def __init__(self, prompt_config) -> None:
        self.prompt = prompt_config

    def __str__(self) -> str:
        return self.prompt

    @abstractmethod
    def desc_prompt(self, func):
        raise NotImplementedError("desc_prompt() is not implemented")

    @abstractmethod
    def execute_prompt(self, func, message):
        raise NotImplementedError("execute_prompt() is not implemented")

    @abstractmethod
    def return_prompt(self, func, message):
        raise NotImplementedError("return_prompt() is not implemented")

    @abstractmethod
    def exception_prompt(self, func, message):
        raise NotImplementedError("exception_prompt() is not implemented")

    @abstractmethod
    def free_prompt(self, func, message):
        raise NotImplementedError("free_prompt() is not implemented")

    @abstractmethod
    def execute_message(self):
        raise NotImplementedError("execute_message() is not implemented")

    @abstractmethod
    def exception_message(self):
        raise NotImplementedError("exception_message() is not implemented")


class LLMBase(ABC):
    def __init__(self, prompt: AskApiPrompt) -> None:
        self.prompt = prompt

    @abstractmethod
    def desc(self, func) -> str:
        raise NotImplementedError("desc() is not implemented")

    @abstractmethod
    def execute_param(self, func, message) -> str:
        raise NotImplementedError("execute() is not implemented")

    @abstractmethod
    def return_value(self, func, message) -> str:
        raise NotImplementedError("return_value() is not implemented")

    @abstractmethod
    def exception(self, func, message) -> str:
        raise NotImplementedError("exception() is not implemented")

    @abstractmethod
    def free_answer(self, func, message) -> str:
        raise NotImplementedError("free_answer() is not implemented")

    def execute_message(self):
        """
        函数开始执行时的提示信息
        :return:
        """
        return self.prompt.execute_message()

    def exception_message(self):
        """
        函数执行异常时的提示信息
        :return:
        """
        return self.prompt.exception_message()


class LLMBuilder(ABC):
    @staticmethod
    def builder_name():
        return "llm_base"

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def __call__(self, prompt_config: Dict) -> LLMBase:
        raise NotImplementedError("__call__() is not implemented")

    @name.setter
    def name(self, value):
        self._name = value



