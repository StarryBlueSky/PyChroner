# coding=utf-8
"""
enum constants
"""

from enum import Enum, IntEnum, unique
from logging import CRITICAL, ERROR, WARN, WARNING, INFO, DEBUG

__all__ = ["PluginType", "API", "LogLevel"]

DiscordPluginTypeIDStart = 50
DiscordPluginTypeIDEnd = 77

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
    TwitterEventMute = 48
    TwitterEventUnmute = 49

    DiscordReady = DiscordPluginTypeIDStart
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
    DiscordServerEmojisUpdate = 69
    DiscordServerAvailable = 70
    DiscordServerUnavailable = 71
    DiscordVoiceStateUpdate = 72
    DiscordMemberBan = 73
    DiscordMemberUnban = 74
    DiscordTyping = 75
    DiscordGroupJoin = 76
    DiscordGroupRemove = DiscordPluginTypeIDEnd

@unique
class DiscordEventFunction(Enum):
    DiscordReady = "on_ready"
    DiscordMessage = "on_message"
    DiscordMessageDelete = "on_message_delete"
    DiscordMessageEdit = "on_message_edit"
    DiscordReactionAdd = "on_reaction_add"
    DiscordReactionRemove = "on_reaction_remove"
    DiscordReactionClear = "on_reaction_clear"
    DiscordChannelCreate = "on_channel_create"
    DiscordChannelDelete = "on_channel_delete"
    DiscordChannelUpdate = "on_channel_update"
    DiscordMemberJoin = "on_member_join"
    DiscordMemberRemove = "on_member_remove"
    DiscordMemberUpdate = "on_member_update"
    DiscordServerJoin = "on_server_join"
    DiscordServerRemove = "on_server_remove"
    DiscordServerUpdate = "on_server_update"
    DiscordServerRoleCreate = "on_server_role_create"
    DiscordServerRoleDelete = "on_server_role_delete"
    DiscordServerRoleUpdate = "on_server_role_update"
    DiscordServerEmojisUpdate = "on_server_emojis_update"
    DiscordServerAvailable = "on_server_available"
    DiscordServerUnavailable = "on_server_unavailable"
    DiscordVoiceStateUpdate = "on_voice_state_update"
    DiscordMemberBan = "on_member_ban"
    DiscordMemberUnban = "on_member_unban"
    DiscordTyping = "on_typing"
    DiscordGroupJoin = "on_group_join"
    DiscordGroupRemove = "on_group_remove"

class DiscordEventFunctionArguments(Enum):
    DiscordReady = []
    DiscordMessage = ["message"]
    DiscordMessageDelete = ["message"]
    DiscordMessageEdit = ["before_message", "after_message"]
    DiscordReactionAdd = ["reaction", "user"]
    DiscordReactionRemove = ["reaction", "user"]
    DiscordReactionClear = ["message", "reactions"]
    DiscordChannelCreate = ["channel"]
    DiscordChannelDelete = ["channel"]
    DiscordChannelUpdate = ["before_channel", "after_channel"]
    DiscordMemberJoin = ["member"]
    DiscordMemberRemove = ["member"]
    DiscordMemberUpdate = ["before_member", "after_member"]
    DiscordServerJoin = ["server"]
    DiscordServerRemove = ["server"]
    DiscordServerUpdate = ["before_server", "after_server"]
    DiscordServerRoleCreate = ["role"]
    DiscordServerRoleDelete = ["role"]
    DiscordServerRoleUpdate = ["before_role", "after_role"]
    DiscordServerEmojisUpdate = ["before_emojis", "after_emojis"]
    DiscordServerAvailable = ["server"]
    DiscordServerUnavailable = ["server"]
    DiscordVoiceStateUpdate = ["before_state", "after_state"]
    DiscordMemberBan = ["member"]
    DiscordMemberUnban = ["server", "user"]
    DiscordTyping = ["channel", "user", "when"]
    DiscordGroupJoin = ["channel", "user"]
    DiscordGroupRemove = ["channel", "user"]

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
