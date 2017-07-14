# coding=utf-8
import copy
from logging import getLogger
from typing import List

from ..datatype.services.discord.account import Account
from .websocket import WebSocket
from ..enums import PluginType, DiscordPluginTypeIDStart, DiscordPluginTypeIDEnd, DiscordEventFunction

logger = getLogger(__name__)

class WebSocketManager:
    def __init__(self, core):
        self.core = core
        self.sockets: List[WebSocket] = []
        self.accounts: List[Account] = []

    def updateAccounts(self, v: Account):
        for us in self.sockets:
            if us.account == v:
                return
        else:
            t = list(copy.deepcopy(self.accounts))
            t.append(v)
            self.accounts = t
            self.run(v)

    def apply(self, ws):
        for pluginType in PluginType:
            if DiscordPluginTypeIDStart <= pluginType.value <= DiscordPluginTypeIDEnd:
                for plugin in self.core.PM.plugins[pluginType.name]:
                    if plugin.meta.discordAccount is ws.account:
                        setattr(ws.client, getattr(DiscordEventFunction, pluginType.name).value, getattr(plugin.module, plugin.meta.functionName))

    def run(self, account):
        ws = WebSocket(self.core, account)
        self.apply(ws)
        self.sockets.append(ws)

        self.core.TM.startThread(ws.start, name=f"StreamingTask_for_{account.key}")
        logger.info(f"Discord {account.id} WebSocket connection has established.")
