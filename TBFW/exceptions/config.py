# coding=utf-8
"""
exception classes about config file.
"""

from . import BaseError
from ..constant import configPath

class NotFoundConfigError(BaseError):
    """
    this exception will raise when config.json is not found.
    """

class InvalidConfigSyntaxError(BaseError):
    """
    this exception will raise when config.json has invalid syntax.
    """

class InvalidLiteralError(BaseError):
    """
    this exception will raise when config.json has invalid literal.
    """

class InsufficientAttributeError(BaseError):
    """
    this exception will raise when config.json lacks an attribute.
    """
    message = "{} lacks an attribute `{}`"

    def __init__(self, attribute: str):
        self.attr = attribute

    def __str__(self):
        return self.message.format(configPath, self.attr)
