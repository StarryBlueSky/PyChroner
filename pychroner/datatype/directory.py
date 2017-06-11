# coding=utf-8
import os
from typing import Dict, List

from . import BaseDataType


class Directory(BaseDataType):
    plugins: str = f"{os.getcwd()}/plugins"
    logs: str = f"{os.getcwd()}/logs"
    tmp: str = f"{os.getcwd()}/tmp"
    cache: str = f"{os.getcwd()}/cache"
    assets: str = f"{os.getcwd()}/assets"
    api: str = f"{os.getcwd()}/api"
    library: str = f"{os.getcwd()}/library"
    original: Dict[str, str] = {}

    def __init__(self, config: Dict[str, str]) -> None:
        self.original = config or {}

        [setattr(self, k, v) for k, v in self.original.items()]

    @property
    def dirs(self) -> List[str]:
        return [self.plugins, self.logs, self.tmp, self.cache, self.assets, self.api, self.library]
