# coding=utf-8
import TBFW

if __name__ == "__main__":
	bot = TBFW.Core()
	while True:
		try:
			bot.Start()
		except TBFW.OutOfMemoryError:
			pass
