# coding=utf-8
import re
import time
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

    def callback(self, stream: Dict) -> None:
        # tweets
        if "text" in stream:
            if stream["user"]["screen_name"] in self.core.config.services.twitter.mute.user_sn \
                or stream["user"]["id"] in self.core.config.services.twitter.mute.user_id \
                or viaPattern.findall(stream["source"])[0] in self.core.config.services.twitter.mute.via \
                or any([domainPattern.findall(entity["expanded_url"])[0] in self.core.config.services.twitter.mute.domain for entity in stream["entities"]["urls"]]):
                    return

            stream["user"]["name"] = stream["user"]["name"].replace("@", "@​")

            # Reply
            if re.match(f"@{self.account.sn}¥s", stream["text"], re.IGNORECASE):
                [
                    self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                    for plugin in self.core.PM.plugins[PluginType.TwitterReply.name]
                    if plugin.meta.twitterAccountName == self.account.key
                ]
            # RT
            if "retweeted_status" in stream:
                [
                    self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                    for plugin in self.core.PM.plugins[PluginType.TwitterRetweet.name]
                    if plugin.meta.twitterAccountName == self.account.key
                ]
            # Timeline
            [
                self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                for plugin in self.core.PM.plugins[PluginType.TwitterTimeline.name]
                if plugin.meta.twitterAccountName == self.account.key
            ]

        # Events
        elif "event" in stream:
            [
                self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                for plugin in self.core.PM.plugins[PluginType.TwitterEvent.name]
                if plugin.meta.twitterAccountName == self.account.key
            ]

        # DM
        elif "direct_message" in stream:
            [
                self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                for plugin in self.core.PM.plugins[PluginType.TwitterDM.name]
                if plugin.meta.twitterAccountName == self.account.key
            ]

        # Miscellaneous UserStream data
        else:
            [
                self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                for plugin in self.core.PM.plugins[PluginType.TwitterMisc.name]
                if plugin.meta.twitterAccountName == self.account.key
            ]

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
