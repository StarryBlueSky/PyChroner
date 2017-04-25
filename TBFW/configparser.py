# coding=utf-8
"""
parse config.json
"""

import json
import os
from typing import List, Dict, Union

from .datatype.account import Account
from .datatype.application import Application
from .datatype.directory import Directory
from .datatype.mute import Mute
from .datatype.slack import Slack
from .enums import LogLevel
from .exceptions.config import *


class Config:
    """
    represent config.json.
    You can access configures with
    
    Example:
    ```python
    config = Config()
    config.accounts.test_bot.ck
    ```
    """
    application: List[Application] = []
    account: List[Account] = []
    mute: Mute = None
    directory: Directory = None
    logLevel: int = None
    slack: Slack = None
    original: Dict[str, Union[str, Dict[str, Dict[str, Union[str, int]]]]] = {}

    def __init__(self):
        if not os.path.isfile(configPath):
            raise NotFoundConfigError(f"{configPath} is not found.")

        try:
            with open(configPath) as f:
                self.original = json.load(f)
        except json.JSONDecodeError:
            raise InvalidConfigSyntaxError(f"{configPath} has invalid syntax.")

        if "accounts" not in self.original:
            raise InsufficientAttributeError("accounts")

        for k, v in self.original["application"].items():
            self.application.append(Application(k, v))

        for k, v in self.original["accounts"].items():
            account: Account = Account(k, v)
            if account.application:
                for application in self.application:
                    if application.key == account.application:
                        account.apply(application)
                        break

            if not account.ck or not account.cs or not account.at or not account.ats \
                    or not account.id or not account.sn:
                raise InsufficientAttributeError("accounts[x].ck, cs, at, ats, id or sn")
            self.account.append(account)

        self.mute = Mute(self.original.get("mute"))
        self.directory = Directory(self.original.get("directory"))
        self.logLevel = getattr(LogLevel, self.original.get("logLevel", "error").title(), LogLevel.Error)
        self.slack = Slack(self.original.get("slack"))

    def get(self, name: str, default: object=None):
        return getattr(self, name, default)

    def reload(self):
        self.__init__()
