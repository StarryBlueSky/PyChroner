# coding=utf-8
"""
exception classes about plugins
"""

from . import BaseError

class InValidPluginFilenameError(BaseError):
    """
    this exception will raise when a plugin's extension is not valid.
    """
    message = "TBFW does not support that plugin's extension. Please check plugin's extension."

class TooManyArgmentsForPluginError(BaseError):
    """
    this exception will raise when a plugin takes too many arguments.
    """
    message = "TBFW could not load plugin because too many argments were required."
