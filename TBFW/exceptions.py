# coding=utf-8

class GeneralError(Exception):
	raise Exception

class OutOfMemoryError(Exception):
	raise MemoryError("TBFW stoped because of out of memory.")

class InValidPluginFilenameError(Exception):
	raise GeneralError("TBFW does not support that plugin's extension. Please check plugin's extension.")

class InvalidPluginSyntaxError(Exception):
	raise SyntaxError("TBFW could not load plugin because of invalid syntax.")
