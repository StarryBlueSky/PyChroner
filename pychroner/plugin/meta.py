# coding=utf-8
import os
from datetime import datetime
from typing import List, Dict, Callable

from .utils import getPluginId
from ..enums import PluginType


class PluginMeta:
    def __init__(self, path: str):
        self.enable = False

        self.path: str = path.replace(os.path.sep, "/")
        self.dir, _, self.filename = self.path.rpartition("/")
        self.pluginDir, _, self.subDir = self.dir.rpartition("/plugins")
        self.subDir = self.subDir[1:]
        self.moduleName, _, self.extension = self.filename.rpartition(".")
        self.id: str = getPluginId(self.path)
        self.accessible = os.path.isfile(self.path)
        self.size: int = os.path.getsize(self.path) if self.accessible else None

        self.type: PluginType = None
        self.priority: int = None
        self.ratio: int = None
        self.hours: List[int] = []
        self.minutes: List[int] = []
        self.multipleHour: int = None
        self.multipleMinute: int = None
        self.permissions: List[Dict] = []
        self.timeout: int = None
        self.validFrom: datetime = None
        self.validUntil: datetime = None
        self.twitterAccount = None
        self.twitterAccountName: str = None
        self.discordAccount = None
        self.discordAccountName: str = None

        self.combinedHours: List[int] = []
        self.combinedMinutes: List[int] = []

        self.function: Callable = None
        self.functionName: str = None
        self.doc: str = None
        self.argumentsCount: int = None

    @property
    def name(self):
        name: str = self.moduleName
        if self.subDir:
            name = f"{self.subDir.replace('_', '')}_{name}"
        if self.functionName and self.functionName != "do":
            name += f"_{self.functionName}"
        return name
