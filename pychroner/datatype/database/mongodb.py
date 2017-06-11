# coding=utf-8
from typing import Dict

from ...datatype import BaseDataType

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None


class MongoDB(BaseDataType):
    host: str = "localhost"
    port: int = 27017
    username: str = None
    password: str = None
    mechanism: str = None
    original: Dict[str, str] = {}

    connect = None
    __db: Dict = {}

    def __init__(self, config: Dict[str, str]) -> None:
        self.original = config or {}

        [setattr(self, k, v) for k, v in self.original.items()]

    def getCollection(self, name: str):
        if not MongoClient:
            raise Exception("pymongo is not found.")

        if not self.connect:
            self.connect = MongoClient(self.host)
        if name not in self.__db:
            self.__db[name] = self.connect[name]
            self.__db[name].authenticate(self.username, self.password, mechanism=self.mechanism)

        return self.__db[name]
