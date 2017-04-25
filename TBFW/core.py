# coding=utf-8
from datetime import datetime
from logging import Logger

from .configparser import Config
from .console import Console
from .enums import PluginType
from .filesystem import FileSystemWatcher
from .plugin.manager import PluginManager
from .thread.manager import ThreadManager
from .utils import getLogger, makeDirs


class Core:
    def __init__(self, prompt: bool=True) -> None:
        self.prompt: bool = prompt
        self.config: Config = Config()

        makeDirs(self.config.directory.dirs)
        self.logger: Logger = getLogger(
                name="TBFW", directory=self.config.directory.logs, logLevel=self.config.logLevel,
                slack=self.config.slack
        )
        self.logger.info(f"Logger started. Current time is {datetime.now()}.")

        self.PM: PluginManager = PluginManager(self)
        self.PM.loadPluginsFromDir()

        self.TM: ThreadManager = ThreadManager(self)

        self.FS: FileSystemWatcher = FileSystemWatcher(self)

        self.console = Console(self, self.prompt)

        self.logger.info(f"Initialization Complate. Current time is {datetime.now()}.")

    def run(self) -> None:
        self.TM.start()
        self.FS.start()
        [
            self.TM.startThread(
                target=getattr(plugin.module, plugin.meta.functionName),
                name=plugin.meta.name,
                keepalive=plugin.meta.type == PluginType.Thread
            )
            for plugin in self.PM.plugins[PluginType.Startup.name] + self.PM.plugins[PluginType.Thread.name]
        ]
        self.TM.startThread(target=self.TM.startSchedulePlugins)

        self.console.loop()
