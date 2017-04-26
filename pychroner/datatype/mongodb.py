# coding=utf-8
from typing import Dict

from . import BaseDataType

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

    def __init__(self, databaseConfig: Dict[str, str]) -> None:
        self.original = databaseConfig

        [setattr(self, k, v) for k, v in self.original.items()]

    def getCollection(self, name: str):
        if not MongoClient:
            raise Exception("pymongo is not found.")

        connect = MongoClient(self.host)
        db = connect[name]
        db.authenticate(self.username, self.password, mechanism=self.mechanism)
        return db
