# coding=utf-8
from pychroner import PluginMeta, PluginType

@PluginMeta(PluginType.Startup, account="Optional")
def do(pluginApi):
    """
    :param pluginApi: pluginApi object.
    """
