# coding=utf-8
import json
import os

TARGET = "TIMELINE"

def do(stream):
	with open("{}/api/stream_timeline.json".format(os.getcwd()), "w") as f:
		json.dump(stream, f)
