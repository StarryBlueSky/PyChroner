# coding=utf-8

class GeneralError(Exception):
	"""
	raise general exceptions
	"""
	raise Exception

class OutOfMemoryError(Exception):
	"""
	raise MemoryError
	"""
	raise MemoryError("TBFW stoped because of out of memory")

