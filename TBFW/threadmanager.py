#  coding=utf-8
import json
import threading
import time
import traceback
from datetime import datetime
from logging import getLogger
from threading import Thread
from typing import List, Tuple, Callable

from .enums import PluginType, API
from .plugin import Plugin
from .plugin.utils import willExecute

logger = getLogger(__name__)

class ThreadManager:
    def __init__(self, core) -> None:
        self.core = core
        self.threads: List[Tuple[Thread, Callable[[], None]]] = []
        self.willExecutePlugins: List[Plugin] = []

    def start(self):
        # noinspection PyTypeChecker
        self.startThread(self.watchThreads)

    def startThread(self, target: Callable, name: str=None, args: List=None, keepalive: bool=True) -> Thread:
        name: str = name or target.__name__
        args: Tuple = tuple(args) if args else ()

        t: Thread = Thread(target=target, name=name, args=args, daemon=True)
        t.start()

        if keepalive:
            self.threads.append((t, target))

        return t

    @staticmethod
    def wrapPlugin(plugin: Plugin) -> None:
        try:
            plugin.module.do()
            logger.info(f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" was executed successfully.")
        except Exception:
            logger.warning(
                f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" "
                f"could not be executed. Error Detail:\n{traceback.format_exc()}"
            )

    def executePluginSafely(self, plugin: Plugin, args: List=None) -> None:
        # noinspection PyTypeChecker
        self.startThread(self.wrapPlugin(plugin), name=plugin.meta.name, args=args or [])

    def destroyThread(self, name: str) -> bool:
        for i, thread, func in enumerate(self.threads):
            if thread.name == name:
                del self.threads[i]
                return True
        return False

    def watchThreads(self) -> None:
        while True:
            try:
                workingThreads: List[Thread] = threading.enumerate()
                with open(f"{self.core.config.directory.api}/{API.Thread.value}", "w") as f:
                    json.dump([x.name for x in workingThreads], f, sort_keys=True, indent=4)

                for i, thread, func in enumerate(self.threads):
                    if not thread.is_alive() or thread not in workingThreads:
                        # noinspection PyTypeChecker
                        self.threads[i] = self.startThread(func, name=thread.name)

            except:
                pass
            finally:
                time.sleep(10)

    def startSchedulePlugins(self):
        while True:
            self.willExecutePlugins = [
                schedulePlugin
                for schedulePlugin in self.core.PM.plugins[PluginType.Schedule.name]
                if willExecute(schedulePlugin.meta.ratio)
            ]

            now: datetime = datetime.now()
            time.sleep(60 - now.second - now.microsecond / 1000000)

            now: datetime = datetime.now()
            [
                self.executePluginSafely(schedulePlugin)
                for schedulePlugin in self.willExecutePlugins
                if now.hour in schedulePlugin.meta.combinedHours
                and now.minute in schedulePlugin.meta.combinedMinutes
            ]
            time.sleep(1)
