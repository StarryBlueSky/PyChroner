# coding=utf-8

def getVariableForEachLocals(__locals__):
	return [{
				"name": key,
				"data": value,
				"type": value.__class__.__name__
	} for key, value in sorted(x for x in __locals__.items() if not x[0].startswith("__") and not x[0].endswith("__"))]
