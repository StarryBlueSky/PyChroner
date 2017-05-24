# coding=utf-8
from flask import Flask
from jinja2 import FileSystemLoader

from pychroner.enums import LogLevel
from .view import View


class WebUIManager:
    app = Flask(__name__)
    app.jinja_loader = FileSystemLoader("pychroner/webui/templates")

    def __init__(self, core):
        self.core = core
        setattr(self.app, "core", self.core)
        View.register(self.app)

    def start(self):
        if self.core.config.logLevel == LogLevel.Debug:
            self.app.debug = True

        self.core.TM.startThread(self.app.run)
