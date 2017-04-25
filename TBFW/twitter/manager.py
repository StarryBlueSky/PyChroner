# coding=utf-8
from typing import List
from ..datatype.account import Account
from .userstream import UserStream

class UserStreamManager:
    def __init__(self, core):
        self.core = core
        self.streams: List[UserStream] = []
        self.accounts: List[Account] = []

    def start(self):
        for account in self.accounts:
            us = UserStream(self.core, account)
            self.streams.append(us)

            self.core.TM.startThread(us.start, name=f"StreamingTask_for_{account.key}")
