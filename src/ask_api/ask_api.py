# -*- coding: utf-8 -*-
"""
ask api, talk with your python code
"""
from ask_api.base.session import Session, Message
from ask_api.llm.llm_util import build_default_llm
from ask_api.base.role import FunctionRole, UserRole, Role
from ask_api.util.askapi_log import logging

GLOBAL_SESSIONS = {}
FUNCTION_ROLES = {}

# 用户角色，目前只用于占位，后续添加交互功能
DEFAULT_USER_ROLE = UserRole("user")


def create_func_role(func, name: str = None) -> Role:
    """
    create function role
    """
    if func in FUNCTION_ROLES:
        return FUNCTION_ROLES[func]

    logging.info("create function role for: {}".format(func.__name__))
    llm = build_default_llm()
    role = FunctionRole(llm, func, name)
    FUNCTION_ROLES[func] = role
    return role


def ask_func(func,
             message: str,
             mode: str = "free",
             user_role: Role = None,
             func_name: str = None,
             session: Session = None) -> Session:
    """
    ask function
    """
    if session is None:
        session_id = str(id(func))
        if session_id not in GLOBAL_SESSIONS:
            GLOBAL_SESSIONS[session_id] = Session()
        session = GLOBAL_SESSIONS[session_id]

    if user_role is None:
        user_role = DEFAULT_USER_ROLE

    if not mode == "desc":
        # 仅在非描述模式下，才将用户输入加入会话
        question = Message(user_role, message)
        session.add_message(question)

    func_role = create_func_role(func, func_name)
    # session 作为参数传入，方便异步函数调用时使用
    answer = func_role.answer(message, mode, session)
    session.add_message(answer)
    return session


def get_session(func):
    """
    get session
    """
    session_id = str(id(func))
    if session_id not in GLOBAL_SESSIONS:
        GLOBAL_SESSIONS[session_id] = Session()
    return GLOBAL_SESSIONS[session_id]
