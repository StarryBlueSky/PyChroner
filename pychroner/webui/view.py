# coding=utf-8
import os
from flask import render_template, send_from_directory
from flask_classy import FlaskView, route, request

class View(FlaskView):
    route_base: str = "/"

    @classmethod
    def register(cls, app, route_base=None, subdomain=None, route_prefix=None, trailing_slash=None):
        super().register(app, route_base, subdomain, route_prefix, trailing_slash)
        cls.core = app.core

    @route("/")
    def page_index(self):
        return render_template(
                "index.html",
                plugins=[plugin for plugins in self.core.PM.plugins.values() for plugin in plugins],
                threads=[x[0].name for x in self.core.TM.threads]
        )

    @route("/execute", methods=["POST"])
    def page_execute(self):
        cmd = request.form["command"]
        self.core.CM.execute(cmd)
        return "Done"

    @route("/static/{name}/{filetype}/<filename>")
    def static(self, name, filetype, filename):
        return send_from_directory(f"{os.getcwd()}/webui/static/{name}/{filetype}", filename)
