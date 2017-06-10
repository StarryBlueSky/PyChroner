# coding=utf-8
"""
exception classes about plugins
"""

from . import BaseError

class NotFoundPluginError(BaseError):
    """
    this exception will raise when a plugin is not found.
    """

class InvalidPluginSyntaxError(BaseError):
    """
    this exception will raise when a plugin has invalid python syntax while loading plugins.
    """

class TimeRelatedArgumentsError(BaseError):
    """
    this exception will raise when a plugin takes time related arguments although it is not Schedule Plugin.
    """

class TimedOut(BaseError):
    """
    this exception will raise when a plugin reaches timed out.
    """
