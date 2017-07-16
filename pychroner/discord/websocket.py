# coding=utf-8
import asyncio

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
                self.loop.run_until_complete(
                        self.client.start(self.account.token)
                )
            except KeyboardInterrupt:
                break
            finally:
                self.loop.run_until_complete(
                        self.client.logout()
                )
                self.loop.close()
