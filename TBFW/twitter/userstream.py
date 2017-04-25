# coding=utf-8
import urllib.parse
import re
from ..enums import PluginType
from typing import Dict

reconnectSecond: int = 5

class UserStream:
    def __init__(self, core, account) -> None:
        self.core = core
        self.account = account
        self.api = self.account.getHandler()

        self.mute = self.core.config.mute.domain

    def callback(self, stream: Dict) -> None:
        try:
            if "text" in stream:
                stream["via"] = re.sub("<.*?>", "", stream["source"])
                if stream["user"]["screen_name"] in self.mute.user_sn \
                    or stream["user"]["id"] in self.mute.user_id \
                    or stream["via"] in self.mute.via:
                    return
                for i in range(len(stream["entities"]["urls"])):
                    if urllib.parse.urlparse(stream["entities"]["urls"][i]["expanded_url"]).hostname in self.mute.domain:
                        return

                stream["user"]["name"] = stream["user"]["name"].replace("@", "@​")

                if re.match("@%s\s" % self.account., stream["text"], re.IGNORECASE):
                    for plugin in self.core.PM.plugins[]:
                        t = threading.Thread(target=self.__executePlugin, name=plugin.attributeName,
                                             args=(plugin, stream,))
                        t.start()
                        break
                    if "dm_obj" in stream:
                        for plugin in Core.plugins[pluginDM]:
                            t = threading.Thread(target=self.__executePlugin, name=plugin.attributeName,
                                                 args=(plugin, stream,))
                            t.start()
                            break
                for plugin in Core.plugins[pluginTimeline]:
                    t = threading.Thread(target=self.__executePlugin, name=plugin.attributeName, args=(plugin, stream,))
                    t.start()

            elif "event" in stream:
                for plugin in Core.plugins[pluginEvent]:
                    t = threading.Thread(target=self.__executePlugin, name=plugin.attributeName, args=(plugin, stream,))
                    t.start()

            elif "direct_message" in stream:

            else:
                for plugin in Core.plugins["other"]:
                    t = threading.Thread(target=self.__executePlugin, name=plugin.attributeName, args=(plugin, stream,))
                    t.start()

        except Exception:
            self.__logger.exception(messageErrorProcessingStream.format(self.sn))

    def start(self) -> None:
        while True:
            try:
                self.api.streaming(self.callback)
            except Exception as e:
                self.core.logger.warning(
                        f"TBFW has been disconnected from UserStream. ({e}) Reconnect in {reconnectSecond}"
                )
