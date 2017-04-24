# coding=utf-8
import time
import inspect
from typing import List
from .command import Command

class Console:
    def __init__(self, core, prompt: bool=True) -> None:
        self.core = core
        self.prompt = prompt
        self.cmd = Command(self.core)
        self.commands = [x[0] for x in inspect.getmembers(self.cmd, inspect.ismethod)]

    def execute(self, text: str) -> None:
        phrases: List[str] = text.split(" ")
        if phrases[0] not in self.commands:
            print(f"Unknown command. Type \"help\" for help.")
            return

        if len(phrases) > 1 and f"{phrases[0]}_{phrases[1]}" in self.commands:
            method: str = f"{phrases[0]}_{phrases[1]}"
            args: List[str] = phrases[2:]
        else:
            method: str = phrases[0]
            args: List[str] = phrases[1:]

        func = getattr(self.cmd, method)
        if func.__code__.co_argcount == 1:
            func()
        else:
            func(args)

    def loop(self):
        if self.prompt:
            while True:
                try:
                    self.execute(input("> "))
                except (KeyboardInterrupt, EOFError):
                    exit(1)
        while True:
            time.sleep(10)
