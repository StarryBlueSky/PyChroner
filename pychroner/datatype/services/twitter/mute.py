# coding=utf-8
from typing import List, Dict, Union, Optional

from ....datatype import BaseDataType


class Mute(BaseDataType):
    via: List[str] = []
    user_id: List[int] = []
    user_sn: List[str] = []
    domain: List[str] = []
    original: Dict[str, List[Union[str, int]]] = {}

    def __init__(self, config: Optional[Dict[str, List[Union[str, int]]]]) -> None:
        muteConfig = config or {}
        self.original = muteConfig

        [setattr(self, k, v) for k, v in self.original.items()]
