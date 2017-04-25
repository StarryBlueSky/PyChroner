# coding=utf-8
from typing import Dict

from . import BaseDataType


class Application(BaseDataType):
    key: str = None
    name: str = None
    ck: str = None
    cs: str = None
    original: Dict[str, str] = {}

    def __init__(self, key: str, applicationConfig: Dict[str, str]) -> None:
        self.original = applicationConfig

        self.key = key
        [setattr(self, k, v) for k, v in self.original.items()]
