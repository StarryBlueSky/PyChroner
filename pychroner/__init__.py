# coding=utf-8
"""
PyChroner library
"""
import sys
ver = sys.version_info
if ver.major < 3 or ver.minor < 6:
    raise Exception("PyChroner requires Python 3.6+.")

requirements = [
    ("requests==2.13.0", "requests"),
    ("watchdog==0.8.3", "watchdog"),
    ("psutil==5.2.2", "psutil"),
    ("gevent==1.2.2", "gevent"),
    ("Flask==0.12.2", "flask"),
    ("Flask-Classy==0.6.10", "flask_classy"),
    ("Jinja2==2.9.6", "jinja2"),
    ("tweepy==3.5.0", "tweepy"),
    ("timeout-decorator==0.3.3", "timeout_decorator"),
    ("discord.py[voice]==0.16.8", "discord")
]

from .pip import PIP
for pipname, modname in requirements:
    try:
        __import__(modname)
    except:
        if PIP.installModule(pipname):
            print("Error occured while installing libraries.")
            exit(1)

from .core import Core as Bot
from .enums import PluginType, API
from .plugin.api import PluginMeta
from .configparser import Config
from .submodules import importModule

__version__ = "3.0.0"
__author__ = "Nephy Project Team"
__license__ = "MIT"
__all__ = ["PluginType", "API", "PluginMeta", "Config", "Bot", "importModule"]
