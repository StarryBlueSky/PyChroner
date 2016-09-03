# coding=utf-8
from TBFW import Bot, TBFWError

if __name__ == "__main__":
	while True:
		try:
			Bot.run()
		except KeyboardInterrupt:
			pass
		except TBFWError as e:
			print(e)
