# coding=utf-8
from TBFW.core import Core as Bot
from TBFW import OutOfMemoryError

if __name__ == "__main__":
	while True:
		try:
			Bot.run()
		except OutOfMemoryError:
			pass
