# coding=utf-8
import os
from typing import List, Dict

from .utils import getPluginId
from ..enums import PluginType


class PluginMeta:
    def __init__(self, path: str):
        self.enable = False

        self.path: str = path.replace(os.path.sep, "/")
        self.dir, _, self.filename = self.path.rpartition("/")
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

        self.combinedHours: List[int] = []
        self.combinedMinutes: List[int] = []

        self.functionName: str = None
        self.doc: str = None
        self.variablesCount: int = None
        self.variablesName: List[str] = []
        self.variables: List = []

    @property
    def name(self):
        return self.moduleName if self.functionName == "do" else f"{self.moduleName}_{self.functionName}"
