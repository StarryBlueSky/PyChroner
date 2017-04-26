# coding=utf-8
"""
PyChroner library
"""
import sys
ver = sys.version_info
if ver.major < 3 or ver.minor < 6:
    raise Exception("PyChroner requires Python 3.6+.")

from .core import Core as Bot
from .enums import PluginType, API
from .plugin.api import PluginMeta
from .configparser import Config
from .submodules import importModule

__version__ = "3.0.0"
__author__ = "Nephy Project Team"
__license__ = "MIT"
__all__ = ["PluginType", "API", "PluginMeta", "Config", "Bot", "importModule"]
