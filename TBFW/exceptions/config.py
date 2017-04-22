# coding=utf-8
"""
exception classes about config file.
"""

from . import BaseError
from ..enums import Path

class NotFoundConfigError(BaseError):
    """
    this exception will raise when config.json is not found.
    """
    message = "{} is not found.".format(Path.Config.value)

class InvalidConfigSyntaxError(BaseError):
    """
    this exception will raise when config.json has invalid syntax.
    """
    message = "{} has invalid syntax.".format(Path.Config.value)

class InsufficientAttributeError(BaseError):
    """
    this exception will raise when config.json lacks an attribute.
    """
    message = "{} lacks an attribute `{}`"

    def __init__(self, attribute: str):
        self.attr = attribute

    def __str__(self):
        return self.message.format(Path.Config.value, self.attr)
