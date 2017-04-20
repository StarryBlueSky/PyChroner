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


def A():
    pass

import os
print(os.path.basename(A.__code__.co_filename)[0:-3])
