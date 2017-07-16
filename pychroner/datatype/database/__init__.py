# coding=utf-8
from .mongodb import MongoDB
from ...datatype import BaseDataType


class DataBase(BaseDataType):
    mongodb: MongoDB = None
