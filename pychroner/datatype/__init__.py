# coding=utf-8
from ..utils import listAttr

class BaseDataType:
    def __str__(self):
        return "\n".join([f"{x.ljust(20)}={getattr(self, x)}" for x in listAttr(self)])
