# coding=utf-8
from logging import CRITICAL, ERROR, WARN, INFO, DEBUG
from enum import Enum, IntEnum, unique, auto

@unique
class PluginType(IntEnum):
    Reply = auto()
    Timeline = auto()
    DM = auto()
    Event = auto()
    Thread = auto()
    Regular = auto()
    Other = auto()
    Initializer = auto()

@unique
class Path(Enum):
    Config = "config.json"
    PluginsDir = "plugins"
    AssetsDir = "assets"
    CacheDir = "cache"
    ApiDir = "api"
    LogDir = "logs"
    TmpDir = "tmp"

@unique
class API(Enum):
    Thread = "thread.json"

class LogLevel(IntEnum):
    Critical = CRITICAL
    Error = ERROR
    Warn = WARN
    Warning = WARN
    Info = INFO
    Debug = DEBUG
