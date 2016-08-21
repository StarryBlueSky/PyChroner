# coding=utf-8
import json

from TBFW.constant import *
from TBFW.exceptions import *


class ConfigParser:
	def __init__(self):
		if not os.path.isfile(pathConfig):
			json.dump({}, open(pathConfig, "w"))

		try:
			config = json.load(open(pathConfig))
		except:
			raise InvalidConfigSyntax

		if not "accounts" in config:
			raise NoAvailableAccountInConfig
		self.accounts = config["accounts"]

		self.muteClient = config.get("muteClient", [])
		self.muteUser = config.get("muteUser", [])
		self.muteDomain = config.get("muteDomain", [])
