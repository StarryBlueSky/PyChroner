# coding=utf-8
from typing import List
from ....datatype import BaseDataType
from .account import Account
from .application import Application
from .mute import Mute

class Twitter(BaseDataType):
    accounts: List[Account] = []
    applications: List[Application] = []
    mute: Mute = None
