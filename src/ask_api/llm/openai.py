# -*- coding: utf-8 -*-
"""
openai based llm
"""
from typing import Dict

import openai
import os

from ask_api.config.askapi_config import ASK_API_DEBUG, DEFAULT_OPENAI_CHAT_MODEL, OPENAI_KEY, OPENAI_KEY_PATH
from ask_api.util.askapi_log import logging
from ask_api.llm.base import LLMBase, AskApiPrompt, LLMBuilder
from ask_api.util.askapi_inspect import get_func_source

# openai api key
if OPENAI_KEY is None:
    if "OPENAI_KEY" in os.environ:
        OPENAI_KEY = os.environ["OPENAI_KEY"]
    elif os.path.exists(OPENAI_KEY_PATH):
        with open(OPENAI_KEY_PATH, "r") as f:
            OPENAI_KEY = f.read().strip()
    else:
        logging.warning(
            "openai key not founded in both os.environ, OPENAI_KEY property and OPENAI_KEY_PATH;  OPENAI_KEY: {}, "
            "OPENAI_KEY_PATH: {}".format(
                OPENAI_KEY, OPENAI_KEY_PATH))
        raise ValueError("openai api key is not available")

openai.api_key = OPENAI_KEY


class OpenAIChatPrompt(AskApiPrompt):
    """
    openai chat prompt
    """
    def __init__(self, prompt_config) -> None:
        """
        Args:
            prompt_config (_type_): _description_
        """
        super().__init__(prompt_config)
        self._system_prompt = self.prompt["system_prompt"]
        self._system_example_prompt = self.prompt["system_example_prompt"]
        self._desc_prompt = self.prompt["desc_prompt"]
        self._execute_prompt = self.prompt["execute_prompt"]
        self._exception_prompt = self.prompt["exception_prompt"]
        self._return_prompt = self.prompt["return_prompt"]

    def _build_system_prompt(self, func, add_example: bool = True):
        """
        build system prompt
        """
        source = get_func_source(func)

        system_prompt = self._system_prompt.format(code_source=source)
        system_prompts = [{"role": "system", "content": system_prompt}]
        if self._system_example_prompt and add_example:
            system_prompts.extend(self._system_example_prompt)

        if ASK_API_DEBUG:
            logging.info("system_prompt: {}".format(system_prompts))

        return system_prompts

    def desc_prompt(self, func):
        desc_prompt = self._desc_prompt
        system_prompts = self._build_system_prompt(func)
        messages = system_prompts + [{"role": "user", "content": desc_prompt}]

        if ASK_API_DEBUG:
            logging.info("desc_prompt: {}".format(messages))

        return messages

    def execute_prompt(self, func, message):
        """
        解析参数的时候不需要拟人化
        Args:
            func (_type_): _description_
            message (_type_): _description_

        Returns:
            _type_: _description_
        """
        execute_prompt = self._execute_prompt.format(message=message)
        system_prompts = self._build_system_prompt(func, add_example=False)
        messages = system_prompts + [{"role": "user", "content": execute_prompt}]

        if ASK_API_DEBUG:
            logging.info("execute_prompt: {}".format(messages))

        return messages

    def return_prompt(self, func, message):
        return_prompt = self._return_prompt.format(message=message)
        system_prompts = self._build_system_prompt(func)
        messages = system_prompts + [{"role": "user", "content": return_prompt}]

        if ASK_API_DEBUG:
            logging.info("return_prompt: {}".format(messages))

        return messages

    def exception_prompt(self, func, message):
        exception_prompt = self._exception_prompt.format(message=message)
        system_prompts = self._build_system_prompt(func)
        messages = system_prompts + [{"role": "user", "content": exception_prompt}]

        if ASK_API_DEBUG:
            logging.info("exception_prompt: {}".format(messages))

        return messages

    def free_prompt(self, func, message):
        free_prompt = [{"role": "user", "content": message}]
        system_prompts = self._build_system_prompt(func)
        messages = system_prompts + free_prompt

        if ASK_API_DEBUG:
            logging.info("free_prompt: {}".format(messages))

        return messages

    def execute_message(self):
        return self.prompt["execute_message"]

    def exception_message(self):
        return self.prompt["exception_message"]


class OpenAIChat(LLMBase):
    """
    Args:
        LLMBase (_type_): _description_
    """

    def __init__(self, prompt: AskApiPrompt, model_name="gpt-3.5-turbo") -> None:
        super().__init__(prompt)
        self.model_name = model_name

    def desc(self, func) -> str:
        desc_prompt_info = self.prompt.desc_prompt(func)
        completion = openai.ChatCompletion.create(model=self.model_name, messages=desc_prompt_info)
        desc_info = completion.choices[0].message.content

        if ASK_API_DEBUG:
            logging.info("desc: {}".format(desc_info))

        return desc_info

    def execute_param(self, func, message) -> str:
        execute_prompt_info = self.prompt.execute_prompt(func, message)
        completion = openai.ChatCompletion.create(model=self.model_name, messages=execute_prompt_info)
        param_info = completion.choices[0].message.content

        if ASK_API_DEBUG:
            logging.info("execute_param: {}".format(param_info))

        return param_info

    def return_value(self, func, message) -> str:
        return_prompt_info = self.prompt.return_prompt(func, message)
        completion = openai.ChatCompletion.create(model=self.model_name, messages=return_prompt_info)
        return_info = completion.choices[0].message.content

        if ASK_API_DEBUG:
            logging.info("return_value: {}".format(return_info))

        return return_info

    def exception(self, func, message) -> str:
        exception_prompt_info = self.prompt.exception_prompt(func, message)
        completion = openai.ChatCompletion.create(model=self.model_name, messages=exception_prompt_info)
        exception_info = completion.choices[0].message.content

        if ASK_API_DEBUG:
            logging.info("exception: {}".format(exception_info))

        return exception_info

    def free_answer(self, func, message) -> str:
        free_prompt_info = self.prompt.free_prompt(func, message)
        completion = openai.ChatCompletion.create(model=self.model_name, messages=free_prompt_info)
        free_answer = completion.choices[0].message.content

        if ASK_API_DEBUG:
            logging.info("free_answer: {}".format(free_answer))

        return free_answer


class OpenAIChatBuilder(LLMBuilder):
    @staticmethod
    def builder_name():
        return "openai_chat"

    """
    OpenAI Chat Builder
    """

    def __init__(self, name: str = "openai_chat", model_name=DEFAULT_OPENAI_CHAT_MODEL) -> None:
        super().__init__(name)
        self.model_name = model_name

    def __call__(self, prompt_config: Dict) -> LLMBase:
        """
        :param prompt_config:
        :return:
        """
        prompt = OpenAIChatPrompt(prompt_config)
        return OpenAIChat(prompt, model_name=self.model_name)
