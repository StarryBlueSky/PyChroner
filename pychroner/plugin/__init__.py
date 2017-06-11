# coding=utf-8
import importlib.util
from logging import getLogger
from typing import List, Callable

from .meta import PluginMeta
from .meta import PluginMeta
from .utils import getPluginId, pluginFilePattern
from ..enums import PluginType
from ..exceptions.plugin import *

logger = getLogger(__name__)

class Plugin:
    def __init__(self, core, path: str) -> None:
        self.isLoaded: bool = False

        self.core = core
        self.meta: PluginMeta = PluginMeta(path=path)
        self.spec = importlib.util.spec_from_file_location(self.meta.name, self.meta.path)

        if not self.meta.accessible:
            raise NotFoundPluginError(f"PyChroner could not find a plugin named {self.meta.name} in {self.meta.path}.")

        if self.spec is None:
            raise ImportError(f"No plugin named {self.meta.name} in {self.meta.path}")

        self.module = importlib.util.module_from_spec(self.spec)
        self.function: Callable = None

    def load(self) -> bool:
        try:
            self.spec.loader.exec_module(self.module)
        except Exception:
            raise InvalidPluginSyntaxError(f"PyChroner could not load a plugin named {self.meta.name} in {self.meta.path}")

        t = [x for x in [getattr(self.module, x) for x in dir(self.module)] if hasattr(x, "__meta__")]
        if len(t) == 0:
            logger.info(f"[Skipped] Module \"{self.meta.name}\"({self.meta.path}) has been skipped.")
            return False
        self.function = t[0]
        for k, v in self.function.__meta__.items():
            setattr(self.meta, k, v)
        self.meta.twitterAccount = self.core.config.getTwitterAccount(self.meta.twitterAccount)

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
        self.meta.enable = True
        logger.info(f"[Loaded] Plugin \"{self.meta.name}\"({self.meta.path}) has been loaded successfully.")
        return self.isLoaded
