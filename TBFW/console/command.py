# coding=utf-8
import threading
from ..plugin.utils import getPluginArgumentCount

class Command:
    def __init__(self, core):
        self.core = core

    def stop(self):
        exit(0)

    def exit(self):
        exit(0)

    def plugin(self):
        print("sub commands: list, info <plugin name>, execute <plugin name>")

    def plugin_info(self, args):
        for pluginType, plugins in self.core.PM.plugins.items():
            for plugin in plugins:
                if plugin.meta.name == args[0]:
                    [print(f"{k.rjust(20)} = {repr(v)}") for k, v in plugin.meta.__dict__.items()]
                    return

    def plugin_list(self):
        for pluginType, plugins in self.core.PM.plugins.items():
            print(f"{pluginType} Plugins:")
            for plugin in plugins:
                print(f"[{'Enabled' if plugin.meta.enable else 'Disabled'}] {plugin.meta.name}")
            print("\n")

    def plugin_execute(self, args):
        for pluginType, plugins in self.core.PM.plugins.items():
            for plugin in plugins:
                if plugin.meta.name == args[0] and getPluginArgumentCount(plugin.meta.type) == 0:
                    plugin.module.do()

    def thread(self):
        print("sub commands: list")

    def thread_list(self):
        print("Active threads:\n")
        [print(x.name) for x in threading.enumerate()]

    def config(self):
        print("sub commands: show, reload")

    def config_show(self):
        [print(f"{k.rjust(20)} = {v}") for k, v in self.core.config.__dict__.items()]

    def config_reload(self):
        self.core.config.reload()
        print("config reloaded.")

    def eval(self, args):
        print(eval(" ".join(args)))
