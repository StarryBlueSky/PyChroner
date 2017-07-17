# coding=utf-8
import time
import copy
from logging import getLogger
from typing import List

from ..plugin.meta import PluginMeta
from ..exceptions.plugin import DiscordEventPluginNeedsExtraArgs
from ..plugin.api import PluginAPI
from ..datatype.services.discord.account import Account
from .websocket import WebSocket
from ..enums import PluginType, DiscordPluginTypeIDStart, DiscordPluginTypeIDEnd, DiscordEventFunction, DiscordEventFunctionArguments

logger = getLogger(__name__)

async def on_error(event: str, *args, **kwargs) -> None:
    logger.exception(f"An error occured while Discord WebSocket ({event}). Event function's args are {args} + {kwargs}.")

def wrap(meta: PluginMeta, pluginType: PluginType, pluginApi):
    args = getattr(DiscordEventFunctionArguments, pluginType.name).value
    if meta.argumentsCount - 1 != len(args):
        raise DiscordEventPluginNeedsExtraArgs(f"Plugin \"{pluginApi.plugin.meta.name}\" needs (pluginApi, {', '.join(args)}) arguments.")

    async def do(*args):
        await meta.function(pluginApi, *args)

    return do

class WebSocketManager:
    def __init__(self, core):
        self.core = core
        self.sockets: List[WebSocket] = []
        self.accounts: List[Account] = []

    def updateAccounts(self, v: Account):
        for account in self.accounts:
            if account == v:
                return
        else:
            self.accounts.append(v)

    def apply(self, ws):
        pluginApi = PluginAPI(self.core)
        pluginApi.discordClient = ws.client

        for pluginType in PluginType:
            if DiscordPluginTypeIDStart <= pluginType.value <= DiscordPluginTypeIDEnd:
                for plugin in self.core.PM.plugins[pluginType.name]:
                    if plugin.meta.discordAccount is ws.account:
                        pluginApi.plugin = plugin
                        try:
                            func = wrap(plugin.meta, pluginType, pluginApi)
                        except DiscordEventPluginNeedsExtraArgs:
                            logger.exception("An error occured while applying Discord event functions.")
                            continue
                        event = getattr(DiscordEventFunction, pluginType.name).value

                        setattr(ws.client, event, func)

        setattr(ws.client, "on_error", on_error)

    def start(self):
        [self.run(account) for account in self.accounts]

    def run(self, account):
        ws = WebSocket(self.core, account)
        self.apply(ws)
        self.sockets.append(ws)

        self.core.TM.startThread(ws.start, name=f"StreamingTask_for_{account.key}")
        logger.info(f"Discord \"{account.id}\" WebSocket connection has established.")
