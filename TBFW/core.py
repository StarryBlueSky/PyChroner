# coding=utf-8
import os
from datetime import datetime
from logging import Logger

from .utils import getLogger
from .configparser import Config
from .enums import PluginType
from .filesystem import FileSystemWatcher
from .plugin.manager import PluginManager
from .threadmanager import ThreadManager
from .console import Console


class Core:
    def __init__(self, prompt: bool=True) -> None:
        self.prompt: bool = prompt
        self.config: Config = Config()

        [
            os.makedirs(x)
            for x in self.config.directory.__dict__.values()
            if not os.path.isdir(x) and not os.path.isfile(x)
        ]

        self.logger: Logger = getLogger("TBFW", directory=self.config.directory.logs, logLevel=self.config.log_level)

        self.PM: PluginManager = PluginManager(self)
        self.PM.loadPluginsFromDir()

        self.TM: ThreadManager = ThreadManager(self)

        self.FS: FileSystemWatcher = FileSystemWatcher(self)

        self.console = Console(self, self.prompt)

        self.logger.info(f"Initialization Complate. Current time is {datetime.now()}.")

    def run(self) -> None:
        [
            self.TM.startThread(
                target=plugin.module.do,
                name=plugin.meta.name,
                keepalive=plugin.meta.type == PluginType.Thread
            )
            for plugin in self.PM.plugins[PluginType.Startup.name] + self.PM.plugins[PluginType.Thread.name]
        ]
        self.TM.startThread(target=self.TM.startSchedulePlugins)

        self.console.loop()
