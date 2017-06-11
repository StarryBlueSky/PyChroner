# coding=utf-8
from typing import Dict, Union

from ....datatype import BaseDataType

class Account(BaseDataType):
    key: str = None
    prefix: str = "!"
    token: str = None
    id: int = None
    original: Dict[str, Union[str, int]] = {}

    def __init__(self, key: str, config: Dict[str, Union[str, int]]) -> None:
        self.original = config

        self.key = key
        [setattr(self, k, v) for k, v in self.original.items()]
