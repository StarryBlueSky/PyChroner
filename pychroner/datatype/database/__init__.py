# coding=utf-8
from ...datatype import BaseDataType
from .mongodb import MongoDB

class DataBase(BaseDataType):
    mongodb: MongoDB = None
