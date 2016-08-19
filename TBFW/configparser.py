# coding=utf-8
import json

class ConfigParser:
	def __init__(self):
		self.config = json.load(open("config.json"))
