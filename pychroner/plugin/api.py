# coding=utf-8
import platform
from datetime import datetime
from logging import getLogger, Logger
from typing import List, Dict, Callable, Optional

from ..datatype.database.mongodb import MongoDB
from ..datatype.logging.slack import Slack
from ..datatype.services.twitter.account import Account
from ..enums import PluginType
from ..exceptions.plugin import TimeRelatedArgumentsError, TimedOut

logger = getLogger(__name__)

def PluginMeta(pluginType: PluginType, timeout: int=None, priority: int=None,
              hours: int=None, minutes: int=None, multipleHour: int=None, multipleMinute: int=None,
              twitterAccount: str=None, ratio: int=None, permissions: List[Dict]=None,
              validFrom: datetime=None, validUntil: datetime=None,
              discordAccount: str=None):
    """
    decorator implementation of plugin metainfo
    :param discordAccount:
    :param validUntil:
    :param validFrom: 
    :param pluginType: (PluginType) target plugin type
    :param timeout: seconds to stop plugin execution
    :param priority: priority to execute plugin (min 0)
    :param hours: 
    :param minutes: 
    :param multipleHour: 
    :param multipleMinute: 
    :param twitterAccount: attached account name
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
            if len(args) > 0 and twitterAccount:
                args[0].twitterAccountName = twitterAccount
            return func(*args)

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
            "twitterAccountName": twitterAccount,
            "discordAccountName": discordAccount,
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

        self.twitterAccountName = None
        self.discordClient = None
        self.plugin = None

    def getTwitterAccount(self, accountKey: str=None) -> Optional[Account]:
        if not self.twitterAccountName and not accountKey:
            return None

        key = accountKey or self.twitterAccountName
        for account in self.config.services.twitter.accounts:
            if account.key == key:
                return account
        return None

    def getDiscordClient(self):
        return self.discordClient

    def getMongoDB(self) -> Optional[MongoDB]:
        return self.config.database.mongodb

    def getSlack(self) -> Optional[Slack]:
        return self.config.logging.slack

    def getLocalStorage(self) -> Optional[Dict]:
        return self.core.LS.get(self.plugin) if self.plugin else None

    def clearLocalStorage(self) -> bool:
        return self.core.LS.clear(self.plugin) if self.plugin else False

    @staticmethod
    def getLogger() -> Logger:
        return logger
