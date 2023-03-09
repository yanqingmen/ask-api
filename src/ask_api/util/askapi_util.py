# -*- coding: utf-8 -*-
"""
util functions for askapi
"""


def get_json_from_text(text: str):
    """
    get json from text
    """
    import json

    json_start = text.find("{")
    json_end = text.rfind("}")
    if json_start == -1 or json_end == -1:
        raise ValueError("json not found")
    else:
        text = text[json_start:json_end + 1]
        return json.loads(text)
