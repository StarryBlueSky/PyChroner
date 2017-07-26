# coding=utf-8
from typing import Dict

class LocalStorage:
    def __init__(self) -> None:
        self.__storage: Dict[str] = {}

    def __get(self, key: str) -> Dict[str]:
        if key not in self.__storage:
            self.__storage[key] = {}
        return self.__storage[key]

    def get(self, plugin) -> Dict[str]:
        return self.__get(plugin.meta.id)

    def __clear(self, key: str) -> bool:
        if key not in self.__storage:
            return False
        del self.__storage[key]
        return True

    def clear(self, plugin) -> bool:
        return self.__clear(plugin.meta.id)
