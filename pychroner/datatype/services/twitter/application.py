# coding=utf-8
from typing import Dict

from ....datatype import BaseDataType


class Application(BaseDataType):
    key: str = None
    ck: str = None
    cs: str = None
    original: Dict[str, str] = {}

    def __init__(self, key: str, config: Dict[str, str]) -> None:
        self.original = config

        self.key = key
        [setattr(self, k, v) for k, v in self.original.items()]
