# coding=utf-8
import os
import json
from gevent.hub import LoopExit
from flask import render_template, send_from_directory, Response
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

    @route("/log")
    def page_log(self):
        return render_template("log.html")

    @route("/api/execute", methods=["POST"])
    def page_execute(self):
        cmd = request.form["command"]
        self.core.CM.execute(cmd)
        return "Done"

    @route("/api/stream")
    def page_stream(self):
        def get():
            q = self.core.queue
            while True:
                try:
                    record = q.get()
                    data = {
                        "time": record.asctime,
                        "line": record.lineno,
                        "log": record.message.replace("\n", "<br>"),
                        "type": record.levelname.lower(),
                        "name": record.name,
                        "thread_name": record.threadName,
                        "function_name": record.funcName,
                        "path": record.pathname
                    }
                    if record.exc_text:
                        data["log"] += "<br>" + record.exc_text.replace("\n", "<br>")
                    yield f"data: {json.dumps(data)}\n\n"
                except LoopExit:
                    return

        return Response(get(), mimetype="text/event-stream")

    @route("/static/{name}/{filetype}/<filename>")
    def static(self, name, filetype, filename):
        return send_from_directory(f"{os.getcwd()}/webui/static/{name}/{filetype}", filename)
