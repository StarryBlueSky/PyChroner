# coding=utf-8
from typing import Callable

def PluginAPI(pluginType, **kwargs):
    def decorator(func: Callable[[], None]):
        def register(*args):
            # noinspection PyUnresolvedReferences
            plugin = {
                "name": func.__name__,
                "doc": func.__doc__,
                "variable": {
                    "count": func.__code__.co_nlocals,
                    "name": list(func.__code__.co_varnames),
                    "value": list(args + func.__code__.co_consts[1:])
                },
                "timeout": kwargs.get("timeout", None),
                "priority": kwargs.get("priority", 0),
                "hours": kwargs.get("hours", []),
                "minutes": kwargs.get("minutes", []),
                "multipleHour": kwargs.get("multipleHour", None),
                "multipleMinute": kwargs.get("multipleMinute", None),
                "account": kwargs.get("account", None),
                "ratio": kwargs.get("ratio", 1),
                "permissions": kwargs.get("permissions", [])
                # {"plugin": "getPingByStatusID", "action": "deny", "users": ["TwitterJP"], "domain": ["following"]}
            }

            print(pluginType.name)
            print(plugin)
            print(kwargs)
            func(*args)
        return register
    return decorator
