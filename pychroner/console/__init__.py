# coding=utf-8
import time
from typing import List

from .command import Command


class ConsoleManager:
    def __init__(self, core) -> None:
        self.core = core
        self.prompt: bool = self.core.prompt
        self.cmd: Command = Command(self.core)

    def execute(self, text: str) -> None:
        phrases: List[str] = [x for x in text.split(" ") if x != ""]
        if not phrases:
            return

        if phrases[0] not in self.cmd.commands:
            method: str = "default"
            args: List[str] = []
        elif len(phrases) > 1 and f"{phrases[0]}_{phrases[1]}" in self.cmd.commands:
            method: str = f"{phrases[0]}_{phrases[1]}"
            args: List[str] = phrases[2:] if len(phrases) >= 3 else []
        else:
            method: str = phrases[0]
            args: List[str] = phrases[1:] if len(phrases) >= 2 else []

        try:
            getattr(self.cmd, method)(*args)
        except Exception as e:
            print(f"Error occured while executing the command. {e}")

    def loop(self) -> None:
        while True:
            try:
                if self.prompt:
                    self.execute(input("> "))
                else:
                    time.sleep(10)
            except (KeyboardInterrupt, EOFError):
                exit(1)
