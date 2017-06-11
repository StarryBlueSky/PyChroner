# coding=utf-8
from ...datatype import BaseDataType
from .slack import Slack
from ...enums import LogLevel

class Logging(BaseDataType):
    level: LogLevel = LogLevel.Error
    slack: Slack = None
