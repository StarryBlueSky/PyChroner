# coding=utf-8
import json
from typing import Dict

import requests

from . import BaseDataType
from ..enums import LogLevel


class Slack(BaseDataType):
    enabled: bool = False
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

    def post(self, text: str, channel: str, username: str=None, icon_emoji: str=None, icon_url: str=None, **kwargs):
        payload = {
            "channel": channel,
            "username": username or "PyChroner Slack Handler",
            "text": text
        }
        if icon_emoji:
            payload["icon_emoji"] = icon_emoji
        elif icon_url:
            payload["icon_url"] = icon_url
        else:
            payload["icon_emoji"] = ":desktop_computer:"
        for k, v in kwargs.items():
            payload[k] = v

        return requests.post(self.webhookUrl, data=json.dumps(payload))
