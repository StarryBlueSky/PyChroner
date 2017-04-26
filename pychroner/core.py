# coding=utf-8
import os
import sys
import platform
from datetime import datetime
from logging import Logger

from .configparser import Config
from .console import ConsoleManager
from .enums import PluginType
from .filesystem import FileSystemWatcher
from .plugin.manager import PluginManager
from .thread.manager import ThreadManager
from .twitter.manager import UserStreamManager
from .utils import getLogger, makeDirs


class Core:
    def __init__(self, prompt: bool=True) -> None:
        self.prompt: bool = prompt
        self.config: Config = Config()
        sys.path.append(self.config.directory.library)

        makeDirs(self.config.directory.dirs)
        self.logger: Logger = getLogger(
                name="pychroner", directory=self.config.directory.logs, logLevel=self.config.logLevel,
                slack=self.config.slack
        )
        self.logger.info(f"Logger started. Current time is {datetime.now()}.")
        self.logger.info(f"Working directory is {os.getcwd()}. Running as {os.getlogin()}, PID {os.getpid()}.")
        self.logger.info(
                f"Operating System is {platform.system()} {platform.release()} "
                f"[version {platform.version()}] ({platform.architecture()[0]}). "
        )
        self.logger.info(
                f"Running Python is version {platform.python_version()} ({platform.python_implementation()}) "
                f"build {platform.python_compiler()} [{ platform.python_build()[1]}]."
        )
        if os.getlogin() == "root":
            self.logger.warning(f"You are running as root. Bot should run as normal user.")

        self.UM: UserStreamManager = UserStreamManager(self)
        self.TM: ThreadManager = ThreadManager(self)

        self.PM: PluginManager = PluginManager(self)
        self.PM.loadPluginsFromDir()

        self.FS: FileSystemWatcher = FileSystemWatcher(self)
        self.CM = ConsoleManager(self)

        self.logger.info(f"Initialization Complate. Current time is {datetime.now()}.")

    def run(self) -> None:
        self.TM.start()
        self.FS.start()
        self.UM.start()
        [
            self.TM.startThread(
                target=getattr(plugin.module, plugin.meta.functionName),
                name=plugin.meta.name,
                keepalive=plugin.meta.type == PluginType.Thread
            )
            for plugin in self.PM.plugins[PluginType.Startup.name] + self.PM.plugins[PluginType.Thread.name]
        ]
        self.TM.startThread(target=self.TM.wrapper.startSchedulePlugins)

        self.CM.loop()
