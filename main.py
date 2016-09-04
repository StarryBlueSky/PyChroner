# coding=utf-8
from TBFW import Bot

if __name__ == "__main__":
	while True:
		try:
			Bot.run()
		except KeyboardInterrupt:
			break
		except:
			pass
