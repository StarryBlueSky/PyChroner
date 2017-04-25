# coding=utf-8
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

    def start(self):
        for account in self.accounts:
            us = UserStream(self.core, account)
            self.streams.append(us)

            self.core.TM.startThread(us.start, name=f"StreamingTask_for_{account.key}")
            logger.info(f"@{account.sn} UserStream connection has established.")
