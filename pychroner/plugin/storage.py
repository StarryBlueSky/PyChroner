# coding=utf-8

class LocalStorage:
    def __init__(self):
        self.__storage = {}

    def __get(self, key: str) -> object:
        if key not in self.__storage:
            self.__storage[key] = {}
        return self.__storage[key]

    def get(self, plugin) -> object:
        return self.__get(plugin.meta.id)
