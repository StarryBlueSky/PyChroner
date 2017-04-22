# coding=utf-8
import traceback

from TBFW.core import Core as Bot

if __name__ == "__main__":
	try:
		Bot.run()
	except Exception:
		print(traceback.format_exc())
