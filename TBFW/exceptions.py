# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class TBFWError(Exception):
	def __init__(self, message):
		self.message = message
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InValidPluginFilenameError(Exception):
	def __init__(self):
		self.message = "TBFW does not support that plugin's extension. Please check plugin's extension."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class NotFoundPluginTargetError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of lacking of `TARGET` variable."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidPluginTargetError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of unsupported target."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidPluginSyntaxError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of invalid syntax."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidPluginScheduleError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of unsupported `HOUR` and `MINUTE` and so on."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class TooManyArgmentsForPluginError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because too many argments were required."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidConfigSyntax(Exception):
	def __init__(self):
		self.message = "TBFW could not start because config.json was invalid."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class NoAvailableAccountInConfig(Exception):
	def __init__(self):
		self.message = "TBFW could not start because there was no account in config."
		logger.exception(self.message)
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message
