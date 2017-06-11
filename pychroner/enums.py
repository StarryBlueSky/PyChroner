# coding=utf-8
"""
enum constants
"""

from enum import Enum, IntEnum, unique
from logging import CRITICAL, ERROR, WARN, WARNING, INFO, DEBUG

__all__ = ["PluginType", "API", "LogLevel"]

@unique
class PluginType(IntEnum):
    """
    represent Plugin's type
    """
    Thread = 0
    Schedule = 1
    Startup = 2

    TwitterReply = 10
    TwitterRetweet = 11
    TwitterTimeline = 12
    TwitterDM = 13
    TwitterFriends = 14
    TwitterDelete = 15
    TwitterStatusWithheld = 16
    TwitterScrubGeo = 17
    TwitterLimit = 18
    TwitterMisc = 19

    TwitterEvent = 20

@unique
class API(Enum):
    """
    represent JSON API filename
    """
    Thread = "thread.json"
    Plugins = "plugins.json"

class LogLevel(IntEnum):
    """
    represent logger levels
    """
    Critical = CRITICAL
    Error = ERROR
    Warn = WARN
    Warning = WARNING
    Info = INFO
    Debug = DEBUG
