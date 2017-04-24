# coding=utf-8
import importlib.util
from logging import getLogger

from typing import List

from ..enums import PluginType
from .utils import getPluginId, pluginFilePattern
from .meta import PluginMeta
from ..exceptions.plugin import *

logger = getLogger(__name__)

class Plugin:
    def __init__(self, path: str) -> None:
        self.isLoaded: bool = False

        self.meta = PluginMeta(path=path)
        self.spec = importlib.util.spec_from_file_location(self.meta.name, self.meta.path)

        if not self.meta.accessible:
            raise NotFoundPluginError(f"TBFW could not find a plugin named {self.meta.name} in {self.meta.path}.")

        if self.spec is None:
            raise ImportError(f"No plugin named {self.meta.name} in {self.meta.path}")

        self.module = importlib.util.module_from_spec(self.spec)

    def load(self) -> bool:
        try:
            self.spec.loader.exec_module(self.module)
        except Exception:
            raise InvalidPluginSyntaxError(f"TBFW could not load a plugin named {self.meta.name} in {self.meta.path}")

        for k, v in self.module.do.__meta__.items():
            setattr(self.meta, k, v)

        if self.meta.type == PluginType.Schedule:
            hours: List[int] = self.meta.hours
            minutes: List[int] = self.meta.minutes

            if self.meta.multipleHour:
                hours += [i * self.meta.multipleHour for i in range(24) if 0 <= i * self.meta.multipleHour < 24]
            if self.meta.multipleMinute:
                minutes += [i * self.meta.multipleMinute for i in range(60) if 0 <= i * self.meta.multipleMinute < 60]

            self.meta.combinedHours = sorted(list(set(hours))) or list(range(24))
            self.meta.combinedMinutes = sorted(list(set(minutes))) or list(range(60))

        self.isLoaded = True
        logger.info(f"[Loaded] Plugin \"{self.meta.name}\"({self.meta.path}) has been loaded successfully.")
        return self.isLoaded
