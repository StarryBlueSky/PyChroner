# coding=utf-8
import copy
from logging import getLogger
from typing import List

from .userstream import UserStream
from ..datatype.account import Account

logger = getLogger(__name__)

class UserStreamManager:
    def __init__(self, core):
        self.core = core
        self.streams: List[UserStream] = []
        self.accounts: List[Account] = []

    def updateAccounts(self, v: Account):
        for us in self.streams:
            if us.account == v:
                return
        else:
            t = list(copy.deepcopy(self.accounts))
            t.append(v)
            self.accounts = t
            self.run(v)

    def run(self, account):
        us = UserStream(self.core, account)
        self.streams.append(us)

        self.core.TM.startThread(us.start, name=f"StreamingTask_for_{account.key}")
        logger.info(f"@{account.sn} UserStream connection has established.")
