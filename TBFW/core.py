# coding=utf-8
import gc
import os
import socket
import time
from datetime import datetime
from logging import getLogger, captureWarnings, Formatter, Logger, Handler
from logging.handlers import RotatingFileHandler
from typing import List

from .configparser import Config
from .enums import PluginType
from .filesystem import FileSystemWatcher
from .plugin.manager import PluginManager
from .threadmanager import ThreadManager
from .utils import willExecute


class Core:
    def __init__(self) -> None:
        self.config: Config = Config()
        self.logger: Logger = self.getLogger()

        [
            os.makedirs(x)
            for x in self.config.directory.__dict__.values()
            if not os.path.isdir(x) and not os.path.isfile(x)
        ]

        self.PM: PluginManager = PluginManager(self)
        self.PM.loadPluginsFromDir()

        self.TM: ThreadManager = ThreadManager(self)

        self.FS: FileSystemWatcher = FileSystemWatcher(self)

        gc.enable()
        socket.setdefaulttimeout(15)

        self.logger.info(f"Initialization Complate. Current time is {datetime.now()}.")

    def getLogger(self) -> Logger:
        logger: Logger = getLogger()
        captureWarnings(capture=True)

        handler: Handler = RotatingFileHandler(
                f"{self.config.directory.logs}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                maxBytes=2 ** 20, backupCount=10000, encoding="utf-8"
        )
        formatter: Formatter = Formatter(
                "[%(asctime)s][%(threadName)s %(name)s/%(levelname)s]: %(message)s",
                "%H:%M:%S"
        )
        handler.setFormatter(formatter)

        logger.setLevel(self.config.log_level)
        logger.addHandler(handler)
        return logger

    def run(self) -> None:
        [
            self.TM.startThread(target=startupPlugin.module.do, name=startupPlugin.meta.name, keepalive=False)
            for startupPlugin in self.PM.plugins[PluginType.Startup.name]
        ]
        [
            self.TM.startThread(target=threadPlugin.module.do, name=threadPlugin.meta.name)
            for threadPlugin in self.PM.plugins[PluginType.Thread.name]
        ]

        self.TM.startThread(target=self.startSchedulePlugins)

        while True:
            try:
                print("> ")
                cmd: str = input()
                print(f"{cmd} is input.")
            except KeyboardInterrupt:
                break

    def startSchedulePlugins(self):
        while True:
            now: datetime = datetime.now()
            willExecutePlugins: List[str] = [
                schedulePlugin.meta.id
                for schedulePlugin in self.PM.plugins[PluginType.Schedule.name]
                if willExecute(schedulePlugin.meta.ratio)
            ]

            time.sleep(60.0 - now.second - now.microsecond / 1000000)

            now: datetime = datetime.now()
            [
                self.TM.executePluginSafely(schedulePlugin)
                for schedulePlugin in self.PM.plugins[PluginType.Schedule.name]
                if schedulePlugin.meta.id in willExecutePlugins
                   and now.hour in schedulePlugin.meta.hours
                   and now.minute in schedulePlugin.meta.minutes
            ]
            time.sleep(1)
