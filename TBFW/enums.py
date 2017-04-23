# coding=utf-8
"""
enum constants
"""

from enum import Enum, IntEnum, unique
from logging import CRITICAL, ERROR, WARN, WARNING, INFO, DEBUG


@unique
class PluginType(IntEnum):
    Reply = 1
    Timeline = 2
    DM = 3
    Event = 4
    Thread = 5
    Schedule = 6
    Startup = 7
    Other = 8

@unique
class API(Enum):
    Thread = "thread.json"
    Plugins = "plugins.json"

class LogLevel(IntEnum):
    Critical = CRITICAL
    Error = ERROR
    Warn = WARN
    Warning = WARNING
    Info = INFO
    Debug = DEBUG
