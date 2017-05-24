# coding=utf-8
import platform
from datetime import datetime
from logging import getLogger
from typing import List, Dict, Callable, Optional

from .utils import getMinPluginArgumentCount
from ..datatype.account import Account
from ..datatype.mongodb import MongoDB
from ..datatype.slack import Slack
from ..enums import PluginType
from ..exceptions.plugin import TooManyArgmentsForPluginError, TimeRelatedArgumentsError, TimedOut

logger = getLogger(__name__)

def PluginMeta(pluginType: PluginType, timeout: int=None, priority: int=None,
              hours: int=None, minutes: int=None, multipleHour: int=None, multipleMinute: int=None,
              account: str=None, ratio: int=None, permissions: List[Dict]=None,
                validFrom: datetime=None, validUntil: datetime=None):
    """
    decorator implementation of plugin metainfo
    :param validUntil: 
    :param validFrom: 
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
            if getMinPluginArgumentCount(pluginType) > len(args):
                raise TooManyArgmentsForPluginError(
                    f"PyChroner could not load plugin "
                    f"because this function takes too many argments."
                )
            if pluginType in [PluginType.Schedule, PluginType.Thread, PluginType.Startup]:
                if func.__code__.co_argcount == 0 or len(args) == 0:
                    return func()
                # PluginAPI
                if hasattr(func, "__meta__"):
                    t = [x for x in args[0].core.config.account if x.key == func.__meta__["account"]]
                    if t:
                        args[0].accountKey = func.__meta__["account"]

                return func(args[0])
            else:
                if func.__code__.co_argcount == 1 or len(args) == 1:
                    # stream
                    return func(args[1])
                # PluginAPI + stream
                if hasattr(func, "__meta__"):
                    t = [x for x in args[0].core.config.account if x.key == func.__meta__["account"]]
                    if t:
                        args[0].accountKey = func.__meta__["account"]
                return func(args[0], args[1])

        if timeout and pluginType is not PluginType.Thread:
            if platform.system() != "Windows":
                import timeout_decorator
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
            "validFrom": validFrom,
            "validUntil": validUntil,

            "function": func,
            "functionName": func.__name__,
            "doc": func.__doc__,
            "argumentsCount": func.__code__.co_argcount,
            "variablesCount": func.__code__.co_nlocals,
            "variablesName": list(func.__code__.co_varnames),
            "variables": list(func.__code__.co_consts[1:]),
        })
        return register
    return decorator

class PluginAPI:
    def __init__(self, core):
        self.core = core

        self.config = self.core.config
        self.dirs = self.config.directory

        self.accountKey = None
        self.plugin = None

    def getAccount(self, accountKey: str=None) -> Optional[Account]:
        if not self.accountKey and not accountKey:
            return None

        key = accountKey or self.accountKey
        for account in self.config.account:
            if account.key == key:
                return account
        return None

    def getMongoDB(self) -> Optional[MongoDB]:
        return self.config.mongodb

    def getSlack(self) -> Optional[Slack]:
        return self.config.slack

    def getLocalStorage(self) -> Optional[Dict]:
        return self.core.LS.get(self.plugin.meta.id) if self.plugin else None
