# coding=utf-8
import os
from typing import List

from . import getPluginId
from ..enums import PluginType


class PluginMeta:
    def __init__(self, path: str):
        self.path: str = path
        self.dir, _, self.filename = self.path.rpartition("/")
        self.name, _, self.extension = self.filename.rpartition(".")
        self.id: str = getPluginId(self.path)
        self.accessible = os.path.isfile(self.path)
        self.size: int = os.path.getsize(self.path) if self.accessible else None

        self.type: PluginType = None
        self.priority: int = None
        self.attachedStream: int = None
        self.ratio: int = None
        self.hour: List[int] = []
        self.minute: List[int] = []
        self.multipleHour: int = None
        self.multipleMinute: int = None
        self.hours: List[int] = []
        self.minutes: List[int] = []
