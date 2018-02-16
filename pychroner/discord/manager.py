# coding=utf-8
import asyncio
from logging import getLogger
from typing import List

from .websocket import WebSocket
from ..datatype.services.discord.account import Account
from ..enums import PluginType, DiscordPluginTypeIDStart, DiscordPluginTypeIDEnd, DiscordEventFunction, DiscordEventFunctionArguments
from ..exceptions.plugin import DiscordEventPluginNeedsExtraArgs
from ..plugin import Plugin
from ..plugin.api import PluginAPI

logger = getLogger(__name__)

async def on_error(event: str, *args, **kwargs) -> None:
    formatted_args = {
        slot: getattr(arg, slot)
        for arg in args for slot in getattr(arg, "__slots__", [])
    }
    logger.exception(f"An error occured while Discord WebSocket ({event}). Event function's args are {formatted_args} + {kwargs}.")


async def wrap(plugin: Plugin, pluginApi: PluginAPI, *args):
    pluginApi.plugin: Plugin = plugin
    try:
        await plugin.meta.function(pluginApi, *args)
    except:
        logger.exception(f"{plugin.meta.type.name} plugin \"{plugin.meta.name}\" could not be executed.")

def apply(ws: WebSocket, plugins: List[Plugin], pluginType: PluginType, pluginApi: PluginAPI):
    default_args: List[str] = getattr(DiscordEventFunctionArguments, pluginType.name).value
    if any([plugin.meta.argumentsCount - 1 != len(default_args) for plugin in plugins]):
        raise DiscordEventPluginNeedsExtraArgs(f"Plugin \"{pluginApi.plugin.meta.name}\" needs (pluginApi, {', '.join(default_args)}) arguments.")

    async def do(*args):
        [asyncio.run_coroutine_threadsafe(wrap(plugin, pluginApi, *args), ws.loop) for plugin in plugins if plugin.meta.discordAccountName == ws.account.key]

    setattr(ws.client, getattr(DiscordEventFunction, pluginType.name).value, do)

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

        # noinspection PyTypeChecker
        for pluginType in PluginType:
            if DiscordPluginTypeIDStart <= pluginType.value <= DiscordPluginTypeIDEnd:
                try:
                    apply(ws, self.core.PM.plugins[pluginType.name], pluginType, pluginApi)
                except DiscordEventPluginNeedsExtraArgs:
                    logger.exception("An error occured while applying Discord event functions.")
                    continue

        setattr(ws.client, "on_error", on_error)

    def start(self):
        [self.run(account) for account in self.accounts]

    def run(self, account):
        ws = WebSocket(self.core, account)
        self.apply(ws)
        self.sockets.append(ws)

        self.core.TM.startThread(ws.start, name=f"StreamingTask_for_{account.key}")
        logger.info(f"Discord \"{account.id}\" WebSocket connection has established.")
