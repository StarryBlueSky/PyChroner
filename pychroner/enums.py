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

    TwitterReply = 10
    TwitterRetweet = 11
    TwitterTimeline = 12
    TwitterDM = 13
    TwitterFriends = 14
    TwitterDelete = 15
    TwitterStatusWithheld = 16
    TwitterScrubGeo = 17
    TwitterLimit = 18
    TwitterMisc = 19

    TwitterEvent = 20
    TwitterFavorite = 21
    TwitterUnfavorite = 22
    TwitterFavoritedRetweet = 23
    TwitterRetweetedRetweet = 24
    TwitterQuotedTweet = 25
    TwitterFollow = 26
    TwitterUserUpdate = 27
    TwitterListMemberAdded = 28

    DiscordReady = 40
    DiscordMessage = 41
    DiscordMessageDelete = 42
    DiscordMessageEdit = 43
    DiscordReactionAdd = 44
    DiscordReactionRemove = 45
    DiscordReactionClear = 46
    DiscordChannelCreate = 47
    DiscordChannelDelete = 48
    DiscordChannelUpdate = 49
    DiscordMemberJoin = 50
    DiscordMemberRemove = 51
    DiscordMemberUpdate = 52
    DiscordServerJoin = 53
    DiscordServerRemove = 54
    DiscordServerUpdate = 55
    DiscordServerRoleCreate = 56
    DiscordServerRoleDelete = 57
    DiscordServerRoleUpdate = 58
    DiscordServerEmojiUpdate = 59
    DiscordServerAvailable = 60
    DiscordServerUnavailable = 61
    DiscordVoiceStateUpdate = 62
    DiscordMemberBan = 63
    DiscordMemberUnban = 64
    DiscordTyping = 65
    DiscordGroupJoin = 66
    DiscordGroupRemove = 67

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
