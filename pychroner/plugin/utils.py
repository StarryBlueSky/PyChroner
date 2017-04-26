# coding=utf-8
import os
import random
import re
from hashlib import sha1

from typing.re import Pattern

from ..datatype.account import Account
from ..enums import PluginType

pluginFilePattern: Pattern = re.compile("^.+[.]py$")

def getPluginId(path: str) -> str:
    return sha1(path.replace(os.path.sep, "/").encode()).hexdigest()

def getMinPluginArgumentCount(pluginType: PluginType) -> int:
    return 1 if pluginType in [PluginType.Reply, PluginType.Timeline, PluginType.Retweet, PluginType.Event,
                               PluginType.DM, PluginType.Other] else 0

def willExecute(ratio: int) -> bool:
    return random.randint(1, ratio) == 1

def serializeDataType(x: object) -> object:
    if isinstance(x, Account):
        return Account.__dict__
