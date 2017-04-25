# coding=utf-8
from typing import Dict, List

from . import BaseDataType


class Directory(BaseDataType):
    plugins: str = "plugins"
    logs: str = "logs"
    tmp: str = "tmp"
    cache: str = "cache"
    assets: str = "assets"
    api: str = "api"
    original: Dict[str, str] = {}

    def __init__(self, directoryConfig: Dict[str, str]=None) -> None:
        directoryConfig = directoryConfig or {}
        self.original = directoryConfig

        [setattr(self, k, v) for k, v in self.original.items()]

    @property
    def dirs(self) -> List[str]:
        return [self.plugins, self.logs, self.tmp, self.cache, self.assets, self.api]
