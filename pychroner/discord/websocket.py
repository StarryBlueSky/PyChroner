# coding=utf-8
import asyncio
import time

from discord.ext import commands


class WebSocket:
    def __init__(self, core, account):
        self.core = core
        self.account = account

        self.loop = asyncio.new_event_loop()
        self.client = commands.Bot(
            loop=self.loop,
            command_prefix=self.account.prefix
        )

    def start(self):
        while True:
            try:
                self.client.run(self.account.token)
            except KeyboardInterrupt:
                break
            finally:
                time.sleep(3)
