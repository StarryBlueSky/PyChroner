# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class InValidPluginFilenameError(Exception):
	def __init__(self):
		self.message = "TBFW does not support that plugin's extension. Please check plugin's extension."
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class NotFoundPluginTargetError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of lacking of `TARGET` variable."
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidPluginTargetError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of unsupported target."
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidPluginSyntaxError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of invalid syntax."
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class InvalidPluginScheduleError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because of unsupported `HOUR` and `MINUTE` and so on."
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message

class TooManyArgmentsForPluginError(Exception):
	def __init__(self):
		self.message = "TBFW could not load plugin because too many argments were required."
		Exception.__init__(self, self.message)

	def __str__(self):
		return self.message
