# coding=utf-8
from . import BaseDataType
from typing import List, Dict, Union

class Mute(BaseDataType):
    via: List[str] = []
    user_id: List[int] = []
    user_sn: List[str] = []
    domain: List[str] = []
    original: Dict[str, List[Union[str, int]]] = {}

    def __init__(self, muteConfig: Dict[str, List[Union[str, int]]]=None) -> None:
        muteConfig = muteConfig or {}
        self.original = muteConfig

        [setattr(self, k, v) for k, v in self.original.items()]
