# coding=utf-8
"""
TBFW library
"""

from .core import Core as Bot
from .enums import PluginType, API
from .plugin.api import PluginAPI
from .configparser import Config
from .submodules import importModule

__version__ = "3.0.0"
__author__ = "Nephy Project Team"
__license__ = "MIT"
__all__ = ["PluginType", "API", "PluginAPI", "Config", "Bot", "importModule"]
