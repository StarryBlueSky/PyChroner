# coding=utf-8
import random
import re
from hashlib import sha1

from typing.re import Pattern
from ..enums import PluginType

pluginFilePattern: Pattern = re.compile("^.+[.]py$")

def getPluginId(name: str):
    return sha1(name.encode()).hexdigest()

def getPluginArgumentCount(pluginType: PluginType) -> int:
    return 1 if pluginType in [PluginType.Reply, PluginType.Timeline, PluginType.Event, PluginType.DM] else 0

def willExecute(ratio: int) -> bool:
    return random.randint(1, ratio) == 1

def getPluginName(path: str):
    return path.replace("\\", "/").split("/")[-1].rpartition(".")[0]
