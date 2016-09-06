# coding=utf-8
import json

from TBFW.constant import apiDir

TARGET = "TIMELINE"

def do(stream):
	with open("{}/stream_timeline.json".format(apiDir), "w") as f:
		json.dump(stream, f)
