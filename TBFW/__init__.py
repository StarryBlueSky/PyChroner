# coding=utf-8
"""
TBFW library
"""

from .enums import Path, PluginType, API
from .plugin import PluginAPI
from .configparser import Config

config = Config()

__version__ = "3.0.0"
__author__ = "Nephy Project Team"
__license__ = "MIT"
__all__ = ["Path", "PluginType", "API", "PluginAPI", "config"]
