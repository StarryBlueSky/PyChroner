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
    Reply = 1
    Timeline = 2
    Retweet = 3
    DM = 4
    Event = 5
    Thread = 6
    Schedule = 7
    Startup = 8
    Other = 9

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
