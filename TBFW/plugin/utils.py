# coding=utf-8
import re
from hashlib import sha1

from typing.re import Pattern

pluginFilePattern: Pattern = re.compile("^.+[.]py$")

def getPluginId(path: str):
    return sha1(path.encode()).hexdigest()
