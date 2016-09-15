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

		if "accounts" not in config:
			raise NoAvailableAccountInConfig
		self.accounts = config["accounts"]
		for account in self.accounts:
			if "ck" in account and "cs" in account and "at" in account and "ats" in account and "sn" in account:
				continue
			else:
				raise InvalidConfigSyntax

		self.muteClient = config.get("muteClient", [])
		self.muteUser = config.get("muteUser", [])
		self.muteDomain = config.get("muteDomain", [])
		self.permissions = config.get("permissions", [])

		self.config = Config()
		setattr(self.config, "muteClient", self.muteClient)
		setattr(self.config, "muteUser", self.muteUser)
		setattr(self.config, "muteDomain", self.muteDomain)
		setattr(self.config, "permissions", self.permissions)
		self.config.accounts = []
		for account in self.accounts:
			cls = Config()
			[setattr(cls, key, value) for key, value in account.items()]
			self.config.accounts.append(cls)
		self.config.permissions = []
		for permission in self.permissions:
			cls = Config()
			[setattr(cls, key, value) for key, value in permission.items()]
			if not getattr(cls, "users"):
				setattr(cls, "users", [])
			if not getattr(cls, "domain"):
				setattr(cls, "domain", [])
			self.config.permissions.append(cls)

class Config:
	pass
