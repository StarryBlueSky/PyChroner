# coding=utf-8
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

class FileSystemWatcher:
    def __init__(self, core) -> None:
        self.core = core

        self.observer: Observer = Observer()
        self.observer.schedule(ChangeHandler(self.core), self.core.config.directory.plugins)

    def start(self) -> None:
        self.observer.start()

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, core) -> None:
        super().__init__()
        self.core = core

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.src_path.endswith(".py"):
            return

        self.core.PM.loadPlugin(path=event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.src_path.endswith(".py"):
            return

        self.core.PM.loadPlugin(path=event.src_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.src_path.endswith(".py"):
            return

        self.core.PM.unloadPlugin(path=event.src_path)
