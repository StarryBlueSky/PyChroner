# coding=utf-8
import threading
import inspect
from ..plugin.utils import getPluginArgumentCount

class Command:
    def __init__(self, core):
        self.core = core
        self.commands = [x[0] for x in inspect.getmembers(self, inspect.isfunction)
                     + inspect.getmembers(self, inspect.ismethod)]
        self.commands.remove("__init__")
        self.commands.remove("default")

    @staticmethod
    def default():
        print(f"Unknown command. Type \"help\" for help.")

    def help(self):
        print("Available commands:")
        print(", ".join(self.commands).replace("_", " "))

    @staticmethod
    def stop():
        exit(0)

    @staticmethod
    def exit():
        exit(0)

    @staticmethod
    def plugin():
        print("sub commands: list, info <plugin name>, execute <plugin name>")

    def plugin_info(self, *args):
        if len(args) < 1:
            print("Type \"plugin info <plugin name>\" to get info.")
            return
        for arg in args:
            found: bool = False
            for pluginType, plugins in self.core.PM.plugins.items():
                for plugin in plugins:
                    if plugin.meta.name == arg:
                        found = True
                        [print(f"{k.rjust(20)} = {repr(v)}") for k, v in plugin.meta.__dict__.items()]
                        break
                if found:
                    break
            else:
                print(f"No such a plugin named \"{arg}\".")

    def plugin_list(self):
        for pluginType, plugins in self.core.PM.plugins.items():
            print(f"{pluginType} Plugins:")
            for plugin in plugins:
                print(f"[{'Enabled' if plugin.meta.enable else 'Disabled'}] {plugin.meta.name}")
            print("\n")

    def plugin_execute(self, *args):
        if len(args) < 1:
            print("Type \"plugin info <plugin name>\" to get info.")
            return
        for arg in args:
            found: bool = False
            for pluginType, plugins in self.core.PM.plugins.items():
                for plugin in plugins:
                    if plugin.meta.name == arg:
                        found = True
                        if getPluginArgumentCount(plugin.meta.type) == 0:
                            getattr(plugin.module, plugin.meta.functionName)()
                        else:
                            print(f"Plugin \"{arg}\" needs an argument. So in this time, could not execute.")
                        break
                if found:
                    break
            else:
                print(f"No such a plugin named \"{arg}\".")

    def plugin_reloadall(self):
        self.core.PM.loadPluginsFromDir()
        print("Reloaded all plugins.")

    @staticmethod
    def thread():
        print("sub commands: list")

    @staticmethod
    def thread_list():
        print("Active threads:\n")
        [print(x.name) for x in threading.enumerate()]

    @staticmethod
    def config():
        print("sub commands: show, reload")

    def config_show(self):
        [print(f"{k.rjust(20)} = {v}") for k, v in self.core.config.__dict__.items()]

    def config_reload(self):
        self.core.config.reload()
        print("config reloaded.")

    def eval(self, *args):
        print(eval(" ".join(args)))
