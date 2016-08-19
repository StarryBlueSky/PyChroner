# coding=utf-8
import os
import gc
import socket
import urllib
import tweepy
import threading
from datetime import datetime
from TBFW.plugin import PluginManager
from TBFW.constant import *
from logging import getLogger, Formatter, FileHandler, INFO, CRITICAL

class Core:
	def __init__(self):
		gc.enable()
		socket.setdefaulttimeout(30)

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-Agent', userAgent), ('Accept-Language', acceptLanguage)]
		urllib.request.install_opener(opener)

		for directory in [pluginsDir, logDir]:
			if not os.path.isdir(directory):
				os.mkdir(directory)

		PM = PluginManager()
		PM.searchAllPlugins()
		self.plugins = PM.plugins
		self.attachedStreamId = PM.attachedStreamId

		self.logPath = logDir + "/" + datetime.now().strftime(messageLogDatetimeFormat) + ".log"
		self.logger = self.__getLogger()

		self.boottime = datetime.now()
		self.logger.info(messageSuccessInitialization.format(self.boottime))

	def __getLogger(self):
		logger = getLogger()
		handler = FileHandler(self.logPath, "w", encoding="utf-8")
		formatter = Formatter(messageLogFormat)
		handler.setFormatter(formatter)

		getLogger("requests").setLevel(CRITICAL)
		getLogger("tweepy").setLevel(CRITICAL)

		logger.addHandler(handler)
		logger.setLevel(INFO)

		return logger

	def run(self):
		db['Set'].update_one({}, {"$set": {"lastrun": datetime.now()}})
		db['Set'].update_one({}, {"$set": {"timed": 0, "threadc": 1, "minly": {"tweet": 0, "event": 0}}})
		Set = db['Set'].find_one()

		auth = tweepy.OAuthHandler(Set['twitterSecret'][0]['ck'], Set['twitterSecret'][0]['cs'])
		auth.set_access_token(Set['twitterSecret'][0]['at'], Set['twitterSecret'][0]['ats'])
		global API
		API = tweepy.API(auth)
		SN = Set['twitterSecret'][0]['screen_name']

		for x in thread_plugin:
			t = x.do()
			t.setName(x.NAME)
			t.start()
		ScheduleTask().start()
		CheckThreading().start()

		event_handler = ChangeHandler()
		observer = Observer()
		observer.schedule(event_handler, pluginsDir, recursive=False)
		observer.start()

		for n in self.attachedStreamId:
			t = threading.Thread(name='Streaming for %s' % n, target=MakeUserStreamConnection, args=(n,))
			t.start()

		while True:
			time.sleep(60)
