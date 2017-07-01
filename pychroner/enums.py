# coding=utf-8
"""
enum constants
"""

from enum import Enum, IntEnum, unique
from logging import CRITICAL, ERROR, WARN, WARNING, INFO, DEBUG

__all__ = ["PluginType", "API", "LogLevel"]

@unique
class PluginType(IntEnum):
    """
    represent Plugin's type
    """
    Thread = 0
    Schedule = 1
    Startup = 2

    Twitter = 10
    TwitterReply = 11
    TwitterRetweet = 12
    TwitterTimeline = 13
    TwitterDM = 14

    TwitterMisc = 20
    TwitterMiscFriends = 21
    TwitterMiscDelete = 22
    TwitterMiscStatusWithheld = 23
    TwitterMiscScrubGeo = 24
    TwitterMiscLimit = 25

    TwitterEvent = 30
    TwitterEventFavorite = 31
    TwitterEventUnfavorite = 32
    TwitterEventFavoritedRetweet = 33
    TwitterEventRetweetedRetweet = 34
    TwitterEventQuotedTweet = 35
    TwitterEventFollow = 36
    TwitterEventUnfollow = 37
    TwitterEventBlock = 38
    TwitterEventUnblock = 39
    TwitterEventUserUpdate = 40
    TwitterEventListCreated = 41
    TwitterEventListUpdated = 42
    TwitterEventListDestroyed = 43
    TwitterEventListMemberAdded = 44
    TwitterEventListMemberRemoved = 45
    TwitterEventListUserSubscribed = 46
    TwitterEventListUserUnsubscribed = 47

    DiscordReady = 50
    DiscordMessage = 51
    DiscordMessageDelete = 52
    DiscordMessageEdit = 53
    DiscordReactionAdd = 54
    DiscordReactionRemove = 55
    DiscordReactionClear = 56
    DiscordChannelCreate = 57
    DiscordChannelDelete = 58
    DiscordChannelUpdate = 59
    DiscordMemberJoin = 60
    DiscordMemberRemove = 61
    DiscordMemberUpdate = 62
    DiscordServerJoin = 63
    DiscordServerRemove = 64
    DiscordServerUpdate = 65
    DiscordServerRoleCreate = 66
    DiscordServerRoleDelete = 67
    DiscordServerRoleUpdate = 68
    DiscordServerEmojiUpdate = 69
    DiscordServerAvailable = 70
    DiscordServerUnavailable = 71
    DiscordVoiceStateUpdate = 72
    DiscordMemberBan = 73
    DiscordMemberUnban = 74
    DiscordTyping = 75
    DiscordGroupJoin = 76
    DiscordGroupRemove = 77

@unique
class API(Enum):
    """
    represent JSON API filename
    """
    Thread = "thread.json"
    Plugins = "plugins.json"

class LogLevel(IntEnum):
    """
    represent logger levels
    """
    Critical = CRITICAL
    Error = ERROR
    Warn = WARN
    Warning = WARNING
    Info = INFO
    Debug = DEBUG
