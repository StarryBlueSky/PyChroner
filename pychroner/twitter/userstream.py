# coding=utf-8
import time
import urllib.parse
from logging import getLogger
import re
from ..enums import PluginType
from typing import Dict

logger = getLogger(__name__)
reconnectSecond: int = 5

class UserStream:
    def __init__(self, core, account) -> None:
        self.core = core
        self.account = account
        self.api = self.account.getHandler()

        self.mute = self.core.config.services.twitter.mute

    def callback(self, stream: Dict) -> None:
        try:
            if "text" in stream:
                if stream["user"]["screen_name"] in self.mute.user_sn \
                    or stream["user"]["id"] in self.mute.user_id \
                    or re.sub("<.+?>", "", stream["source"]) in self.mute.via \
                    or any([urllib.parse.urlparse(stream["entities"]["urls"][i]["expanded_url"]).hostname in self.mute.domain for i in range(len(stream["entities"]["urls"]))]):
                        return

                stream["user"]["name"] = stream["user"]["name"].replace("@", "@​")

                if re.match(f"@{self.account.sn}¥s", stream["text"], re.IGNORECASE):
                    [
                        self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                        for plugin in self.core.PM.plugins[PluginType.TwitterReply.name]
                        if plugin.meta.twitterAccount == self.account
                    ]
                if "retweeted_status" in stream:
                    [
                        self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                        for plugin in self.core.PM.plugins[PluginType.TwitterRetweet.name]
                        if plugin.meta.twitterAccount == self.account
                    ]
                [
                    self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                    for plugin in self.core.PM.plugins[PluginType.TwitterTimeline.name]
                    if plugin.meta.twitterAccount == self.account
                ]

            elif "event" in stream:
                [
                    self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                    for plugin in self.core.PM.plugins[PluginType.TwitterEvent.name]
                    if plugin.meta.twitterAccount == self.account
                ]

            elif "direct_message" in stream:
                [
                    self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                    for plugin in self.core.PM.plugins[PluginType.TwitterDM.name]
                    if plugin.meta.twitterAccount == self.account
                ]

            else:
                [
                    self.core.TM.wrapper.executePluginSafely(plugin, [stream])
                    for plugin in self.core.PM.plugins[PluginType.TwitterOther.name]
                    if plugin.meta.twitterAccount == self.account
                ]

        except Exception:
            logger.exception(f"Error occured while processing @{self.account.sn} UserStream.")

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
