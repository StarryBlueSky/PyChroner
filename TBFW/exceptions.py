# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class OutOfMemoryError(Exception):
	raise MemoryError("TBFW stoped because of out of memory.")

class InValidPluginFilenameError(Exception):
	raise Exception("TBFW does not support that plugin's extension. Please check plugin's extension.")

class InvalidPluginTargetError(Exception):
	raise SyntaxError("TBFW could not load plugin because of unsupported target.")

class InvalidPluginSyntaxError(Exception):
	raise SyntaxError("TBFW could not load plugin because of invalid syntax.")
