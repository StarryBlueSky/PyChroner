# coding=utf-8
import time
import traceback
from datetime import datetime
from logging import getLogger
from typing import List

from ..enums import PluginType
from ..plugin import Plugin
from ..plugin.utils import willExecute

logger = getLogger(__name__)

class ThreadWrapper:
    def __init__(self, core):
        self.core = core

    @staticmethod
    def wrap(plugin: Plugin, *args) -> None:
        try:
            print(args)
            getattr(plugin.module, plugin.meta.functionName)(*args)
            logger.info(f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" was executed successfully.")
        except Exception:
            logger.warning(
                f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" "
                f"could not be executed. Error Detail:\n{traceback.format_exc()}"
            )

    def executePluginSafely(self, plugin: Plugin, args: List=None) -> None:
        # noinspection PyTypeChecker
        if args:
            args = [plugin] + args
        else:
            args = [plugin]
        self.core.TM.startThread(self.wrap, name=plugin.meta.name, args=args)

    def startSchedulePlugins(self):
        while True:
            self.core.TM.willExecutePlugins = [
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
