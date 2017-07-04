# coding=utf-8
import os
import platform
import sys
from datetime import datetime
from logging import Logger

import psutil
from gevent.queue import Queue

from .configparser import Config
from .console import ConsoleManager
from .enums import PluginType
from .filesystem import FileSystemWatcher
from .plugin.api import PluginAPI
from .plugin.manager import PluginManager
from .plugin.storage import LocalStorage
from .thread.manager import ThreadManager
from .twitter.manager import UserStreamManager
from .utils import getLogger, makeDirs
from .webui.manager import WebUIManager


class Core:
    def __init__(self, prompt: bool=True) -> None:
        pidFile = f"{os.getcwd()}/lock"
        if os.path.isfile(pidFile):
            running = False
            with open(pidFile) as f:
                pid = f.read()
                if pid.isdigit() and psutil.pid_exists(int(pid.strip())):
                    running = True
            if running:
                print("PyChroner is already running.")
                exit(1)
        with open(pidFile, "w") as f:
            f.write(str(os.getpid()))

        self.prompt: bool = prompt
        self.config: Config = Config()
        sys.path.append(self.config.directory.library)

        makeDirs(self.config.directory.dirs)
        self.queue = Queue()
        self.logger: Logger = getLogger(
                name="pychroner", directory=self.config.directory.logs, logLevel=self.config.logging.level,
                slack=self.config.logging.slack,
                queue=self.queue
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
        if os.getlogin() in ["root", "Administrator"]:
            self.logger.warning(f"You are running as root or Administrator. Bot should be running as a normal user.")

        self.UM: UserStreamManager = UserStreamManager(self)
        self.TM: ThreadManager = ThreadManager(self)

        self.PM: PluginManager = PluginManager(self)
        self.PM.loadPluginsFromDir()

        self.FS: FileSystemWatcher = FileSystemWatcher(self)
        self.CM = ConsoleManager(self)
        self.WM = WebUIManager(self)
        self.LS = LocalStorage()

        self.logger.info(f"Initialization Complate. Current time is {datetime.now()}.")

    def run(self) -> None:
        self.TM.start()
        self.FS.start()
        [
            self.TM.startThread(
                target=getattr(plugin.module, plugin.meta.functionName),
                name=plugin.meta.name,
                keepalive=plugin.meta.type == PluginType.Thread,
                args=[PluginAPI(self)]
            )
            for plugin in self.PM.plugins[PluginType.Startup.name] + self.PM.plugins[PluginType.Thread.name]
        ]
        self.TM.startThread(target=self.TM.wrapper.startSchedulePlugins)

        if self.config.webui.enabled:
            self.WM.start()
        self.CM.loop()
