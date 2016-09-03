# coding=utf-8
from TBFW import Bot, TBFWError

if __name__ == "__main__":
	while True:
		try:
			Bot.run()
		except TBFWError:
			pass
