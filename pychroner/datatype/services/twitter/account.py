# coding=utf-8
from typing import Dict, Union

import tweepy

from ....datatype.services.twitter.application import Application
from ....datatype import BaseDataType
from ....twitter import twispy


class Account(BaseDataType):
    key: str = None
    application: Union[str, Application] = None
    ck: str = None
    cs: str = None
    at: str = None
    ats: str = None
    id: int = None
    sn: str = None
    original: Dict[str, Union[str, int]] = {}

    def __init__(self, key: str, config: Dict[str, Union[str, int]]) -> None:
        self.original = config

        self.key = key
        [setattr(self, k, v) for k, v in self.original.items()]

    def apply(self, application: Application):
        if application.key == self.application:
            self.application = application
            self.ck = application.ck
            self.cs = application.cs
            return
        raise KeyError("application name is not valid.")

    def getHandler(self) -> twispy.handler.API:
        return twispy.handler.API(self.ck, self.cs, self.at, self.ats)

    def getTweepyHandler(self) -> tweepy.API:
        if not tweepy:
            raise Exception("tweepy is not found.")
        auth = tweepy.OAuthHandler(self.ck, self.cs)
        auth.set_access_token(self.at, self.ats)

        return tweepy.API(auth)
