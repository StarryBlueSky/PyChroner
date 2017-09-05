# coding=utf-8
import time
from datetime import datetime
from logging import getLogger
from typing import List

from ..enums import PluginType
from ..plugin import Plugin
from ..plugin.api import PluginAPI
from ..plugin.utils import willExecute

logger = getLogger(__name__)

class ThreadWrapper:
    def __init__(self, core):
        self.core = core

    def wrap(self, plugin: Plugin, *args) -> None:
        try:
            api = PluginAPI(self.core)
            api.plugin = plugin
            args = [api] + list(args)
            plugin.meta.function(*args)
            if plugin.meta.type is PluginType.Schedule:
                logger.info(f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" has been executed successfully.")
        except Exception:
            logger.exception(
                f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" could not be executed."
            )

    def executePluginSafely(self, plugin: Plugin, args: List=None) -> None:
        if plugin.meta.validUntil and plugin.meta.validUntil < datetime.now():
            return
        if plugin.meta.validFrom and plugin.meta.validFrom > datetime.now():
            return
        args: List = [plugin] + args if args else [plugin]
        self.core.TM.startThread(self.wrap, name=plugin.meta.name, args=args)

    def startSchedulePlugins(self):
        while True:
            self.core.TM.willExecutePlugins: List[Plugin] = [
                schedulePlugin
                for schedulePlugin in self.core.PM.plugins[PluginType.Schedule.name]
                if willExecute(schedulePlugin.meta.ratio)
            ]

            now: datetime = datetime.now()
            time.sleep(60 - now.second - now.microsecond / 1000000)

            now: datetime = datetime.now()
            [
                self.executePluginSafely(schedulePlugin)
                for schedulePlugin in self.core.TM.willExecutePlugins
                if now.hour in schedulePlugin.meta.combinedHours
                and now.minute in schedulePlugin.meta.combinedMinutes
            ]
            time.sleep(1)
