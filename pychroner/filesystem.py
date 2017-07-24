# coding=utf-8
import time

from watchdog.events import FileSystemEvent, RegexMatchingEventHandler
from watchdog.observers import Observer


class FileSystemWatcher:
    def __init__(self, core) -> None:
        self.core = core

        self.observer: Observer = Observer()
        self.observer.schedule(ChangeHandler(self.core), self.core.config.directory.plugins, recursive=True)

    def start(self) -> None:
        self.observer.start()

class ChangeHandler(RegexMatchingEventHandler):
    def __init__(self, core) -> None:
        super().__init__(regexes=["^.+[.]py$"], ignore_directories=True)
        self.core = core

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.event_type in ["created", "modified"]:
            time.sleep(1)
            self.core.PM.loadPlugin(path=event.src_path)
            [self.core.WSM.apply(ws) for ws in self.core.WSM.sockets]

        elif event.event_type == "deleted":
            self.core.PM.unloadPlugin(path=event.src_path)
