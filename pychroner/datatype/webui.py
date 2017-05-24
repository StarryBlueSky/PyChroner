# coding=utf-8
from typing import Dict
from . import BaseDataType

class WebUI(BaseDataType):
    enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 5000
    original: Dict[str, str] = {}

    def __init__(self, config: Dict[str, str]) -> None:
        self.original = config or {}

        [setattr(self, k, v) for k, v in self.original.items()]
