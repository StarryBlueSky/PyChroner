# coding=utf-8
"""
parse config.json
"""

import json
import os

from .enums import LogLevel
from .exceptions.config import *
from .utils import listAttr, convertDictToObject, ConvertedObject


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

    def __init__(self):
        if not os.path.isfile(Path.Config.value):
            raise NotFoundConfigError

        try:
            with open(Path.Config.value) as f:
                config = convertDictToObject(json.load(f))
        except json.JSONDecodeError:
            raise InvalidConfigSyntaxError

        if not hasattr(config, "accounts"):
            raise InsufficientAttributeError("accounts")

        for k in listAttr(config.accounts):
            v = getattr(config.accounts, k)
            if hasattr(v, "application") and hasattr(config, "application"):
                app = getattr(config.application, v.application)
                if not app:
                    raise InsufficientAttributeError("application")
                if not hasattr(app, "ck") or not hasattr(app, "cs"):
                    raise InsufficientAttributeError("accounts[x].ck or accounts[x].cs")

                v.ck, v.cs = app.ck, app.cs

            for attr in ["ck", "cs", "at", "ats", "id", "sn"]:
                if not hasattr(v, attr):
                    raise InsufficientAttributeError("accounts[x].{}".format(attr))
            setattr(config.accounts, k, v)

        if not hasattr(config, "mute"):
            config.mute = ConvertedObject()
        for attr in ["via", "user_id", "user_sn", "domain"]:
            hasattr(config.mute, attr) or setattr(config.mute, attr, [])

        # TODO: implement permissions

        if not hasattr(config, "log_level"):
            setattr(config, "log_level", LogLevel.Error)
        elif not hasattr(LogLevel, config.log_level.title()):
            config.log_level = LogLevel.Error
        else:
            config.log_level = getattr(LogLevel, config.log_level.title())

        [setattr(self, x, getattr(config, x)) for x in listAttr(config)]
