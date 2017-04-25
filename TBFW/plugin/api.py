# coding=utf-8
import platform
from logging import getLogger
from typing import List, Dict, Callable

import timeout_decorator

from .utils import getPluginArgumentCount
from ..enums import PluginType
from ..exceptions.plugin import TooManyArgmentsForPluginError, TimeRelatedArgumentsError, TimedOut

logger = getLogger(__name__)

def PluginAPI(pluginType: PluginType, timeout: int=None, priority: int=None,
              hours: int=None, minutes: int=None, multipleHour: int=None, multipleMinute: int=None,
              account: str=None, ratio: int=None, permissions: List[Dict]=None):
    """
    decorator implementation of plugin metainfo
    :param pluginType: (PluginType) target plugin type
    :param timeout: seconds to stop plugin execution
    :param priority: priority to execute plugin (min 0)
    :param hours: 
    :param minutes: 
    :param multipleHour: 
    :param multipleMinute: 
    :param account: attached account name
    :param ratio: possibility of 1/n to execute plugin
    :param permissions: {"action": "deny", "user_id": [10000000], "user_sn": ["TwitterJP"], "domain": ["following"]}
    :return: 
    """

    if pluginType is not PluginType.Schedule and any([hours, minutes, multipleHour, multipleMinute]):
        raise TimeRelatedArgumentsError(
            "Time related arguments are only able "
            "to be set when pluginType is not PluginType.Schedule."
        )

    def decorator(func: Callable):
        def register(*args) -> Callable:
            if getPluginArgumentCount(pluginType) != len(args):
                raise TooManyArgmentsForPluginError(
                    f"TBFW could not load plugin "
                    f"because this function takes too many argments."
                )

        if timeout and pluginType is not PluginType.Thread:
            if platform.system() != "Windows":
                register = timeout_decorator.timeout(timeout, timeout_exception=TimedOut)(register)
            else:
                logger.warning("Timeout feature is disabled in Windows.")

        setattr(register, "__meta__", {
            "type": pluginType,
            "priority": priority or 0,
            "ratio": ratio or 1,
            "hours": hours or [],
            "minutes": minutes or [],
            "multipleHour": multipleHour,
            "multipleMinute": multipleMinute,
            "permissions": permissions or [],
            "account": account,
            "timeout": timeout,

            "functionName": func.__name__,
            "doc": func.__doc__,
            "variablesCount": func.__code__.co_nlocals,
            "variablesName": list(func.__code__.co_varnames),
            "variables": list(func.__code__.co_consts[1:]),
        })
        return register
    return decorator
