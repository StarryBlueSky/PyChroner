# coding=utf-8
"""
parse config.json
"""

import json
import os
from typing import Dict, Union

from .datatype.services import Services
from .datatype.database import DataBase
from .datatype.logging import Logging
from .datatype.directory import Directory
from .datatype.secret import Secret
from .datatype.webui import WebUI
from .datatype.services.twitter.account import Account
from .datatype.logging.slack import Slack
from .enums import LogLevel
from .exceptions.config import *

configPath = "config.json"

class Config:
    """
    represent config.json.
    """
    services: Services = Services()
    database: DataBase = DataBase()
    directory: Directory = Directory()
    webui: WebUI = None
    secret: Secret = None
    logging: Logging = Logging()
    original: Dict[str, Union[str, Dict[str, Dict[str, Union[str, int]]]]] = {}

    def __init__(self):
        if not os.path.isfile(configPath):
            raise NotFoundConfigError(f"{configPath} is not found.")

        try:
            with open(configPath, encoding="utf-8") as f:
                self.original = json.load(f)
        except json.JSONDecodeError:
            raise InvalidConfigSyntaxError(f"{configPath} has invalid syntax.")

        for service, t in self.original.get("services", {}).items():
            if service == "twitter":
                from .datatype.services.twitter.mute import Mute
                from .datatype.services.twitter.application import Application
                from .datatype.services.twitter.account import Account

                self.services.twitter.mute = Mute(t.get("mute"))
                self.services.twitter.applications = [Application(k, v) for k, v in t["applications"].items()]

                for k, v in t["accounts"].items():
                    account: Account = Account(k, v)
                    if account.application:
                        for application in self.services.twitter.applications:
                            if application.key == account.application:
                                account.apply(application)
                                break

                    if not account.ck or not account.cs or not account.at or not account.ats or not account.id or not account.sn:
                        raise InsufficientAttributeError("services.twitter.accounts.x.ck, cs, at, ats, id or sn")
                    self.services.twitter.accounts.append(account)

            elif service == "discord":
                from .datatype.services.discord.account import Account

                for k, v in t["accounts"].items():
                    account: Account = Account(k, v)
                    self.services.discord.accounts.append(account)

        for database, t in self.original.get("database", {}).items():
            if database == "mongodb":
                from .datatype.database.mongodb import MongoDB

                self.database.mongodb = MongoDB(t)

        self.logging.level = getattr(LogLevel, self.original.get("logging", {}).get("level", "error").title(), LogLevel.Error)
        self.logging.slack = Slack(self.original.get("logging", {}).get("slack"))

        self.secret = Secret(self.original.get("secret"))
        self.webui = WebUI(self.original.get("webui"))

    def get(self, name: str, default: object=None) -> object:
        return getattr(self, name, default)

    def getTwitterAccount(self, name: str) -> Account:
        for account in self.services.twitter.accounts or {}:
            if account.key == name:
                return account

    def reload(self):
        self.__init__()
