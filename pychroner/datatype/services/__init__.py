# coding=utf-8
from ...datatype import BaseDataType
from .twitter import Twitter
from .discord import Discord

class Services(BaseDataType):
    twitter: Twitter = Twitter()
    discord: Discord = Discord()
