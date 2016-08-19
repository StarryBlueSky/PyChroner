# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class OutOfMemoryError(Exception):
	raise MemoryError("TBFW stoped because of out of memory.")

class InValidPluginFilenameError(Exception):
	raise FileNotFoundError("TBFW does not support that plugin's extension. Please check plugin's extension.")

class NotFoundPluginTargetError(Exception):
	raise SyntaxError("TBFW could not load plugin because of lacking of `TARGET` variable.")

class InvalidPluginTargetError(Exception):
	raise NotImplementedError("TBFW could not load plugin because of unsupported target.")

class InvalidPluginSyntaxError(Exception):
	raise SyntaxError("TBFW could not load plugin because of invalid syntax.")

class InvalidPluginScheduleError(Exception):
	raise NotImplementedError("TBFW could not load plugin because of unsupported `HOUR` and `MINUTE` and so on.")

class TooManyArgmentsForPluginError(Exception):
	raise NotImplementedError("TBFW could not load plugin because too many argments were required.")
