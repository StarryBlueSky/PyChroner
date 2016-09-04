# coding=utf-8
import traceback
from TBFW import Bot

if __name__ == "__main__":
	try:
		Bot.run()
	except:
		print(traceback.format_exc())
