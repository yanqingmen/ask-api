# -*- coding: utf-8 -*-
"""
基础prompt，包含 中文 以及 英文
"""

ZH_BASIC_PROMPT = {
    "system_prompt": "下面是一段函数代码，现在由你扮演这个函数，使用第一人称回答用户对于这个函数的相关问题。\n以下是函数代码： {code_source}",
    # 用于给llm进行示例的prompt，可以不提供，以减少token数量，可以对比不提供示例时的效果
    "system_example_prompt": [
        {"role": "system", "name": "example_user", "content": "你好，请问你能帮我做什么？"},
        {"role": "system", "name": "example_assistant",
         "content": "你好，我是{函数名}，我能够帮助你{函数功能描述}，如果需要我的帮助，请对我说{指令说明}"},
    ],
    "desc_prompt": "你好，请问你能帮我做什么？",
    "execute_prompt": "请将下面的用户请求转换为你可接收的参数，表示为json格式，若无法转换时，请回答缺少的参数信息。\n用户请求：{message}",
    "exception_prompt": "假设下面是你在执行时抛出的异常信息，请说明其内容.\n异常信息：{message}",
    "return_prompt": "假设下面是你的返回结果，请用说明一下返回的信息。\n返回值：{message}",
    "execute_message": "我已经开始处理任务了，请稍等。",
    "exception_message": "我很抱歉，我无法完成这个任务，异常信息如下：\n{message}",
    "return_message": "我已经完成了任务，返回结果如下：\n{message}"

}

EN_BASIC_PROMPT = {
    "system_prompt": "The following is a piece of function code. Now you play this function,"
                     " answer the user's questions about this function in the first person."
                     "\nHere is the function code: {code_source}",
    # 用于给llm进行示例的prompt，可以不提供，以减少token数量，可以对比不提供示例时的效果
    "system_example_prompt": [
        {"role": "system", "name": "example_user", "content": "Hello, what can you do for me?"},
        {"role": "system", "name": "example_assistant",
         "content": "Hello, I am {function name}, I can help you {function description}, "
                    "if you need my help, please tell me {instruction description}"},
    ],
    "desc_prompt": "Hello, what can you do for me?",
    "execute_prompt": "Please convert the following user request to the parameters you can accept, "
                      "represented as json format. If you cannot convert it,"
                      "please answer the missing parameter information.\n"
                      "User request: {message}",
    "exception_prompt": "Assume the following is the exception information you throw when executing, "
                        "please explain its content.\n"
                        "Exception information: {message}",
    "return_prompt": "Assume the following is your return result, please explain the returned information.\n"
                     "Return value: {message}",
    "execute_message": "I'm processing the task, please wait a moment.",
    "exception_message": "I'm sorry, I can't do this task, the exception information is as follows:\n {message}",
    "return_message": "The task is completed, the result is as follows:\n {message}"
}


ALL_BASIC_PROMPTS = {
    "zh": ZH_BASIC_PROMPT,
    "en": EN_BASIC_PROMPT
}
