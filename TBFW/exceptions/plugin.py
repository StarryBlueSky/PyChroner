# coding=utf-8
"""
exception classes about plugins
"""

from . import BaseError

class InvalidPluginExtensionError(BaseError):
    """
    this exception will raise when a plugin's extension is not allowed.
    """

class NotFoundPluginError(BaseError):
    """
    this exception will raise when a plugin is not found.
    """

class InvalidPluginSyntaxError(BaseError):
    """
    this exception will raise when a plugin has invalid python syntax while loading plugins.
    """

class TooManyArgmentsForPluginError(BaseError):
    """
    this exception will raise when a plugin takes too many arguments.
    """
    message = "TBFW could not load plugin because too many argments were required."
