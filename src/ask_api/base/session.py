# -*- coding: utf-8 -*-
"""
会话管理，记录历史会话信息
"""
from typing import List


class Message(object):
    def __init__(self, role, text, task=None) -> None:
        self.role = role
        self.text = text
        # 异步任务
        self.task = task

    def __str__(self) -> str:
        return str(self.role) + ": " + self.text

    def __repr__(self) -> str:
        return str(self.role) + ": " + self.text

    def get_role(self):
        return self.role

    def get_text(self):
        return self.text

    def get(self):
        return self.role, self.text

    def set_role(self, role):
        self.role = role

    def set_text(self, text):
        self.text = text

    def set(self, role, text):
        self.role = role
        self.text = text

    def set_task(self, task):
        self.task = task

    def get_task(self):
        return self.task


class Session(object):
    def __init__(self) -> None:
        self.messages = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages(self) -> List[Message]:
        return self.messages

    def print_messages(self):
        print("*" * 40 + "Session" + "*" * 40)
        for message in self.messages:
            print(message)
        print("*" * 40 + "Session" + "*" * 40)

    def get_current(self) -> Message:
        return self.messages[-1]
