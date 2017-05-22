# coding=utf-8
from pychroner import PluginMeta, PluginType

@PluginMeta(PluginType.Schedule, account="Optional", hours=[], minutes=[], multipleHour=None, multipleMinute=None)
def do(pluginApi):
    """
    :param pluginApi: pluginApi object.
    """
