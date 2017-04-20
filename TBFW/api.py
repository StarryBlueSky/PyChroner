# coding=utf-8
from typing import Callable

from .enums import PluginType

def Plugin(**kwargs):
    def decorator(func: Callable[[], None]):
        def register():
            if func.__code__.co_argcount != 0:
                raise Exception("Too many arguments (Takes only 1 argument)")

            plugin = {
                "name": func.__name__,
                "doc": func.__doc__,
                "variable": {
                    "count": func.__code__.co_nlocals,
                    "name": func.__code__.co_varnames,
                    "value": func.__code__.co_consts[1:]
                }
            }

            print(plugin)
            print(kwargs)
            func()
        return register
    return decorator

def PluginMeta
