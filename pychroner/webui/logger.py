# coding=utf-8
from logging import Handler

from gevent.queue import Queue

class QueueHandler(Handler):
    def __init__(self, queue: Queue):
        Handler.__init__(self)

        self.queue = queue

    def emit(self, record):
        self.queue.put_nowait(record)
