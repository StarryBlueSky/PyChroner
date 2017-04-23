# coding=utf-8
import json
import logging
import os
from typing import Dict, List

from . import Plugin, getPluginId
from ..enums import PluginType, API

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self, core):
        self.core = core
        self.plugins: Dict[str, List[Plugin]] = None
        self.unloadPlugins()

    def unloadPlugins(self) -> None:
        # noinspection PyTypeChecker
        self.plugins: Dict[str, List[Plugin]] = {x.name: [] for x in PluginType}

    def loadPlugin(self, path: str) -> bool:
        plugin: Plugin = Plugin(path=path)
        plugin.load()

        # noinspection PyTypeChecker
        for pluginType in PluginType:
            for i, loadedPlugin in enumerate(self.plugins[pluginType.name]):
                if plugin.meta.id == loadedPlugin.meta.id:
                    self.plugins[pluginType.name][i] = plugin
                    break
        else:
            self.plugins[plugin.meta.type.name].append(plugin)

        # noinspection PyTypeChecker
        self.plugins = {pluginType.name: sorted(self.plugins[pluginType.name], key=lambda x: x.meta.priority, reverse=True) for pluginType in PluginType}

        with open(f"{self.core.config.directory.api}/{API.Thread.name}", "w") as f:
            # noinspection PyTypeChecker
            json.dump([plugin.meta.__dict__ for pluginType in PluginType for plugin in self.plugins[pluginType.name]], f, sort_keys=True, indent=4)
        return True

    def unloadPlugin(self, path: str) -> bool:
        pluginId: str = getPluginId(path=path)

        # noinspection PyTypeChecker
        for pluginType in PluginType:
            for i, plugin in enumerate(self.plugins[pluginType.name]):
                if plugin.meta.id == pluginId:
                    del self.plugins[pluginType.name][i]
                    logger.info(f"[Unloaded] Plugin \"{plugin.meta.name}\"({plugin.meta.path}) has been unloaded successfully.")
                    return True
        logger.warning(f"Plugin \"{plugin.meta.name}\"({plugin.meta.path}) could not be unloaded because it is not loaded.")
        return False

    def loadPluginsFromDir(self) -> bool:
        self.unloadPlugins()

        for pluginFile in os.listdir(self.core.config.directory.plugins):
            pluginPath: str = f"{self.core.config.directory.plugins}/{pluginFile}"
            self.loadPlugin(pluginPath)

        return True
