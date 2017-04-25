# coding=utf-8
from typing import Dict

from . import BaseDataType
from ..enums import LogLevel


class Slack(BaseDataType):
    webhookUrl: str = None
    channel: str = None
    username: str = None
    iconEmoji: str = None
    iconUrl: str = None
    logLevel: int = None
    original: Dict[str, str] = {}

    def __init__(self, slackConfig: Dict[str, str]=None) -> None:
        slackConfig = slackConfig or {}
        self.original = slackConfig

        [setattr(self, k, v) for k, v in self.original.items()]
        self.logLevel = getattr(LogLevel, self.original.get("logLevel", "error").title(), LogLevel.Error)
