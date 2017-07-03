# coding=utf-8
import re
import time
import urllib.parse
from typing import Dict

from typing.re import Pattern

from ..enums import PluginType

reconnectSecond: int = 5

viaPattern: Pattern = re.compile("<.+?>")
domainPattern: Pattern = re.compile("https?://([^/]+).*")

class UserStream:
    def __init__(self, core, account) -> None:
        self.core = core
        self.account = account
        self.api = self.account.getHandler()

    def callPlugins(self, pluginType: PluginType, stream: Dict):
        [
            self.core.TM.wrapper.executePluginSafely(plugin, [stream])
            for plugin in self.core.PM.plugins[pluginType.name]
            if plugin.meta.twitterAccountName == self.account.key
        ]

    def callback(self, stream: Dict) -> None:
        # tweets
        if "text" in stream:
            if stream["user"]["screen_name"] in self.core.config.services.twitter.mute.user_sn \
                or stream["user"]["id"] in self.core.config.services.twitter.mute.user_id \
                or viaPattern.sub("\1", stream["source"]) in self.core.config.services.twitter.mute.via \
                or any([urllib.parse.urlparse(entity["expanded_url"]).hostname in self.core.config.services.twitter.mute.domain for entity in stream["entities"]["urls"]]):
                    return

            # prevent Name-Reply attack
            stream["user"]["name"] = stream["user"]["name"].replace("@", "@​")

            # Reply
            if re.match(f"@{self.account.sn}¥s", stream["text"], re.IGNORECASE):
                self.callPlugins(PluginType.TwitterReply, stream)
            # RT
            if "retweeted_status" in stream:
                self.callPlugins(PluginType.TwitterRetweet, stream)

            # All Timeline
            self.callPlugins(PluginType.TwitterTimeline, stream)

        # DM
        elif "direct_message" in stream:
            self.callPlugins(PluginType.TwitterDM, stream)

        # Events
        elif "event" in stream:
            if stream["event"] == "favorite":
                self.callPlugins(PluginType.TwitterEventFavorite, stream)
            elif stream["event"] == "unfavorite":
                self.callPlugins(PluginType.TwitterEventUnfavorite, stream)
            elif stream["event"] == "favorited_retweet":
                self.callPlugins(PluginType.TwitterEventFavoritedRetweet, stream)
            elif stream["event"] == "retweeted_retweet":
                self.callPlugins(PluginType.TwitterEventRetweetedRetweet, stream)
            elif stream["event"] == "quoted_tweet":
                self.callPlugins(PluginType.TwitterEventQuotedTweet, stream)
            elif stream["event"] == "follow":
                self.callPlugins(PluginType.TwitterEventFollow, stream)
            elif stream["event"] == "unfollow":
                self.callPlugins(PluginType.TwitterEventUnfollow, stream)
            elif stream["event"] == "block":
                self.callPlugins(PluginType.TwitterEventBlock, stream)
            elif stream["event"] == "unblock":
                self.callPlugins(PluginType.TwitterEventUnblock, stream)
            elif stream["event"] == "user_update":
                self.callPlugins(PluginType.TwitterEventUserUpdate, stream)
            elif stream["event"] == "list_created":
                self.callPlugins(PluginType.TwitterEventListCreated, stream)
            elif stream["event"] == "list_updated":
                self.callPlugins(PluginType.TwitterEventListUpdated, stream)
            elif stream["event"] == "list_destroyed":
                self.callPlugins(PluginType.TwitterEventListDestroyed, stream)
            elif stream["event"] == "list_member_added":
                self.callPlugins(PluginType.TwitterEventListMemberAdded, stream)
            elif stream["event"] == "list_member_removed":
                self.callPlugins(PluginType.TwitterEventListMemberRemoved, stream)
            elif stream["event"] == "list_user_subscribed":
                self.callPlugins(PluginType.TwitterEventListUserSubscribed, stream)
            elif stream["event"] == "list_user_unsubscribed":
                self.callPlugins(PluginType.TwitterEventListUserUnsubscribed, stream)

            # All Events
            self.callPlugins(PluginType.TwitterEvent, stream)

        # Miscellaneous UserStream data
        else:
            if "friends" in stream:
                self.callPlugins(PluginType.TwitterMiscFriends, stream)
            elif "delete" in stream:
                self.callPlugins(PluginType.TwitterMiscDelete, stream)
            elif "status_withheld" in stream:
                self.callPlugins(PluginType.TwitterMiscStatusWithheld, stream)
            elif "scrub_geo" in stream:
                self.callPlugins(PluginType.TwitterMiscScrubGeo, stream)
            elif "limit" in stream:
                self.callPlugins(PluginType.TwitterMiscLimit, stream)

            # All Miscs
            self.callPlugins(PluginType.TwitterMisc, stream)

        # All UserStream data
        self.callPlugins(PluginType.Twitter, stream)

    def start(self) -> None:
        while True:
            try:
                self.api.streaming(self.callback)
            except Exception as e:
                self.core.logger.warning(
                        f"PyChroner has been disconnected from UserStream. ({e}) Reconnect in {reconnectSecond} secs."
                )
            finally:
                time.sleep(reconnectSecond)
