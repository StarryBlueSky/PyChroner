# coding=utf-8
import re
from typing import Dict

class ConvertedObject:
    pass

def convertDictToObject(x: Dict) -> object:
    y = ConvertedObject()

    for k, v in x.items():
        if isinstance(v, dict):
            v = convertDictToObject(v)
        setattr(y, k, v)

    return y

def listAttr(x: object) -> list:
    return [y for y in dir(x) if not y.startswith("__") and not y.endswith("__")]

def isSafeLiteral(x: str) -> bool:
    m = re.match("^\w+$", x)
    m2 = re.match("^[^\d]", x)
    return True if m and m2 else False
