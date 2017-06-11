# coding=utf-8
from typing import List
from ....datatype import BaseDataType
from .account import Account

class Discord(BaseDataType):
    accounts: List[Account] = []
