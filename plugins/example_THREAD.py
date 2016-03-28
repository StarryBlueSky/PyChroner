# -*- coding: utf-8 -*-
import os
import threading
import time

TARGET = 'THREAD'

#クラス名はdo
class do(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			try:
				#Botが動いている間、60秒おきにfreeします
				os.system('free')
				time.sleep(60)
			except:
				pass