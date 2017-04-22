# coding=utf-8
from enum import Enum, unique

@unique
class PluginType(Enum):
    Reply = 1
    Timeline = 2
    DM = 3
    Event = 4
    Thread = 5
    Regular = 6
    Other = 7
    Initializer = 8

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
