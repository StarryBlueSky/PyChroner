# coding=utf-8
import json
import logging
import os
import traceback
from typing import Dict, List

from . import Plugin
from .utils import getPluginId, pluginFilePattern, serializeDataType, willExecute
from ..enums import PluginType, API
from ..exceptions.plugin import InvalidPluginSyntaxError

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
        plugin: Plugin = Plugin(self.core, path=path)
        try:
            t: bool = plugin.load()
        except InvalidPluginSyntaxError:
            logger.warning(
                f"Plugin {path} "
                f"could not be loaded because it has invalid syntax. "
                f"Error Detail:\n{traceback.format_exc()}."
            )
            return False
        if not t:
            return False

        found: bool = False
        # noinspection PyTypeChecker
        for pluginType in PluginType:
            for i, loadedPlugin in enumerate(self.plugins[pluginType.name]):
                if plugin.meta.id == loadedPlugin.meta.id:
                    found = True
                    self.plugins[pluginType.name][i] = plugin
                    for j, x in enumerate(self.core.TM.willExecutePlugins):
                        if x.meta.id == plugin.meta.id:
                            self.core.TM.willExecutePlugins[j] = plugin

                    if PluginType.Thread == pluginType:
                        pass
                        # TODO: kill the thread

                    break
            if found:
                break
        else:
            self.plugins[plugin.meta.type.name].append(plugin)
            if plugin.meta.type is PluginType.Schedule and willExecute(plugin.meta.ratio):
                self.core.TM.willExecutePlugins.append(plugin)

        if plugin.meta.account:
            self.core.UM.updateAccounts(plugin.meta.account)

        # noinspection PyTypeChecker
        self.plugins = {
            pluginType.name: sorted(
                    self.plugins[pluginType.name],
                    key=lambda x: x.meta.priority, reverse=True
            ) for pluginType in PluginType}

        with open(f"{self.core.config.directory.api}/{API.Plugins.value}", "w") as f:
            # noinspection PyTypeChecker
            json.dump([
                plugin.meta.__dict__
                for pluginType in PluginType for plugin in self.plugins[pluginType.name]
            ], f, sort_keys=True, indent=4, default=serializeDataType)
        return True

    def unloadPlugin(self, path: str) -> bool:
        pluginId: str = getPluginId(path)

        # noinspection PyTypeChecker
        for pluginType in PluginType:
            for i, plugin in enumerate(self.plugins[pluginType.name]):
                if plugin.meta.id == pluginId:
                    for j, x in enumerate(self.core.TM.willExecutePlugins):
                        if x.meta.id == pluginId:
                            del self.core.TM.willExecutePlugins[j]

                    # TODO: kill the thread

                    logger.info(
                        f"[Unloaded] Plugin \"{plugin.meta.name}\"({plugin.meta.path}) "
                        f"has been unloaded successfully."
                    )
                    del self.plugins[pluginType.name][i]
                    return True
        logger.warning(
            f"Plugin \"{pluginId}\" "
            f"could not be unloaded because it is not loaded."
        )
        return False

    def loadPluginsFromDir(self) -> bool:
        self.unloadPlugins()

        for root, _, contents in os.walk(self.core.config.directory.plugins):
            for content in contents:
                path: str = os.path.join(root, content)
                if pluginFilePattern.match(path) and os.path.isfile(path):
                    self.loadPlugin(path)

        return True
