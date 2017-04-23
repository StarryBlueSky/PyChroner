# coding=utf-8
import importlib.util
import re
from hashlib import sha1
from logging import getLogger

from typing.re import Pattern

from .meta import PluginMeta
from .module import PluginModule
from ..exceptions.plugin import *

logger = getLogger(__name__)

pluginFilePattern: Pattern = re.compile("^.+[.]py$")

def getPluginId(path: str):
    return sha1(path.encode()).hexdigest()

class Plugin:
    def __init__(self, path: str) -> None:
        self.isLoaded: bool = False

        self.module: module = PluginModule()
        self.meta = PluginMeta(path=path)

        if not self.meta.accessible:
            raise NotFoundPluginError(f"TBFW could not find a plugin named {self.meta.name} in {self.meta.path}.")

        if pluginFilePattern.match(self.meta.filename) is None:
            raise InvalidPluginExtensionError(f"TBFW does not support this plugin's extension. Please check this plugin's extension. ({self.meta.path})")

    @property
    def isLoaded(self) -> bool:
        return self.isLoaded

    @isLoaded.setter
    def isLoaded(self, v: bool):
        self.isLoaded = v

    def load(self) -> bool:
        spec = importlib.util.spec_from_file_location(self.meta.name, self.meta.path)
        if spec is None:
            raise ImportError(f"No plugin named {self.meta.name} in {self.meta.path}")

        plugin = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(plugin)
        except Exception:
            raise InvalidPluginSyntaxError(f"TBFW could not load a plugin named {self.meta.name} in {self.meta.path}")

        self.module, self.isLoaded = plugin, True
        logger.info(f"[Loaded] Plugin \"{self.meta.name}\"({self.meta.path}) has been loaded successfully.")
        return self.isLoaded

        # if not hasattr(plugin, pluginAttributeTarget):
        #     raise NotFoundPluginTargetError
        # if getattr(plugin, pluginAttributeTarget).lower() not in pluginTypes:
        #     raise InvalidPluginTargetError
        # self.attributeTarget = getattr(plugin, pluginAttributeTarget)
        # self.attributeType = self.attributeTarget.lower()
        #
        # if self.attributeType in [pluginReply, pluginTimeline, pluginEvent, pluginOther]:
        #     maxArgs = 1
        # else:
        #     maxArgs = 0
        # if plugin.do.__code__.co_argcount != maxArgs:
        #     raise TooManyArgmentsForPluginError
        #
        # self.attributePriority = getattr(plugin, pluginAttributePriority, defaultAttributePriority)
        # if self.attributeType in [pluginReply, pluginTimeline, pluginEvent, pluginOther]:
        #     self.attributeAttachedStream = getattr(plugin, pluginAttributeAttachedStream, defaultAttributeAttachedStream)
        # self.attributeRatio = getattr(plugin, pluginAttributeRatio, defaultAttributeRatio)
        # if type(self.attributeRatio).__name__ != "int":
        #     raise InvalidPluginRatioError
        #
        # if self.attributeType == pluginRegular:
        #     hours = []
        #     minutes = []
        #     pluginHour = getattr(plugin, pluginAttributeHour, defaultAttributeHour)
        #     pluginMinute = getattr(plugin, pluginAttributeMinute, defaultAttributeMinute)
        #     pluginMultipleHour = getattr(plugin, pluginAttributeMultipleHour, defaultAttributeMultipleHour)
        #     pluginMultipleMinute = getattr(plugin, pluginAttributeMultipleMinute, defaultAttributeMultipleMinute)
        #
        #     if pluginHour != defaultAttributeHour:
        #         if isinstance(pluginHour, list):
        #             hours.extend(pluginHour)
        #         elif isinstance(pluginHour, int):
        #             hours.append(pluginHour)
        #         else:
        #             raise InvalidPluginScheduleError
        #
        #     if pluginMinute != defaultAttributeMinute:
        #         if isinstance(pluginMinute, list):
        #             minutes.extend(pluginMinute)
        #         elif isinstance(pluginMinute, int):
        #             minutes.append(pluginMinute)
        #         else:
        #             raise InvalidPluginScheduleError
        #
        #     if pluginMultipleHour != defaultAttributeMultipleHour:
        #         if isinstance(pluginMultipleHour, int):
        #             hours.extend(
        #                 [i * pluginMultipleHour for i in range(oneDayHours) if dayStartHour <= i * pluginMultipleHour < oneDayHours]
        #             )
        #         else:
        #             raise InvalidPluginScheduleError
        #
        #     if pluginMultipleMinute != defaultAttributeMultipleMinute:
        #         if isinstance(pluginMultipleMinute, int):
        #             minutes.extend(
        #                 [i * pluginMultipleMinute for i in range(oneHourMinutes) if dayStartHour <= i * pluginMultipleMinute < oneHourMinutes]
        #             )
        #         else:
        #             raise InvalidPluginScheduleError
        #
        #     hours = sorted(list(set(hours)))
        #     minutes = sorted(list(set(minutes)))
        #     if not hours:
        #         hours = list(range(oneDayHours))
        #     if not minutes:
        #         minutes = list(range(oneHourMinutes))
        #     self.attributeHours = hours
        #     self.attributeMinutes = minutes
