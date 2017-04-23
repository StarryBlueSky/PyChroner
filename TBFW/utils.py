# coding=utf-8
import random
import re
from typing import Dict, Match

from .exceptions.config import InvalidLiteralError


class ConvertedObject:
    pass

def convertDictToObject(x: Dict) -> object:
    y: ConvertedObject = ConvertedObject()

    for k, v in x.items():
        if isinstance(v, dict):
            v: Dict = convertDictToObject(v)

        if not isSafeLiteral(k):
            raise InvalidLiteralError(f"`{k}` is invalid literal.")
        setattr(y, k, v)

    return y

def listAttr(x: object) -> list:
    return [y for y in dir(x) if not y.startswith("__") and not y.endswith("__")]

def isSafeLiteral(x: str) -> bool:
    m: Match = re.match("^\w+$", x)
    m2: Match = re.match("^[^\d]", x)
    return m is not None and m2 is not None

def willExecute(ratio: int) -> bool:
    return random.randint(1, ratio) == 1
