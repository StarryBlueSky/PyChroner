# coding=utf-8
import gc
import re
import json
import random
import socket
import threading
import time
import traceback
import urllib
from datetime import datetime
from logging import getLogger, captureWarnings, Formatter, INFO, CRITICAL
from logging.handlers import RotatingFileHandler

from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer

from TBFW.constant import *
from TBFW.plugin import PluginManager

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

		self.PM = PluginManager()
		self.PM.searchAllPlugins()
		self.plugins = self.PM.plugins
		self.attachedStreamId = self.PM.attachedStreamId

		# connect = MongoClient(DBInfo.Host)
		# self.db = connect.bot
		# self.db.authenticate(DBInfo.Username, DBInfo.Password, mechanism=DBInfo.Method)
		# self.Set = db['Set'].find_one()

		# db['Set'].update_one({}, {"$set": {"lastrun": datetime.now()}})
		# db['Set'].update_one({}, {"$set": {"timed": 0, "threadc": 1, "minly": {"tweet": 0, "event": 0}}})

		self.logPath = logDir + "/" + datetime.now().strftime(messageLogDatetimeFormat) + ".log"
		self.__logger = self.__getLogger()

		self.boottime = datetime.now()
		self.__logger.info(messageSuccessInitialization.format(self.boottime))

	def __getLogger(self):
		logger = getLogger()
		captureWarnings(True)

		handler = RotatingFileHandler(self.logPath, maxBytes=20, encoding="utf-8")
		formatter = Formatter(messageLogFormat)
		handler.setFormatter(formatter)

		getLogger("requests").setLevel(CRITICAL)
		getLogger("tweepy").setLevel(CRITICAL)

		logger.setLevel(INFO)
		logger.addHandler(handler)

		return logger

	def run(self):
		for threadPlugin in self.plugins[pluginThread]:
			t = threadPlugin.do()
			t.setName(threadPlugin.attributeName)
			t.start()
		threading.Thread(name="__scheduleRegularPlugins", target=self.__scheduleRegularPlugins, args=()).start()
		threading.Thread(name="__watchThreadActivity", target=self.__watchThreadActivity, args=()).start()

		observer = Observer()
		observer.schedule(self.ChangeHandler(regexes=["\.py$"]), pluginsDir, recursive=False)
		observer.start()

		for n in self.attachedStreamId:
			t = threading.Thread(name='Streaming for %s' % n, target=MakeUserStreamConnection, args=(n,))
			t.start()

		while True:
			time.sleep(60)

	def __scheduleRegularPlugins(self):
		logger = self.__logger

		def _do(plugin):
			try:
				plugin.code.do()
				logger.info(messageSuccessExecutingRegularPlugin.format(plugin.attributeName))
			except:
				logger.warning(messageErrorExecutingRegularPlugin.format(plugin.attributeName, traceback.format_exc()))

		while True:
			wait_time = 60 - datetime.now().second
			time.sleep(wait_time)
			datetime_hour = datetime.now().hour
			datetime_minute = datetime.now().minute
			for regularPlugin in self.plugins["regular"]:
				if random.randint(1, regularPlugin.attributeRatio) != 1:
					continue
				if datetime_hour in regularPlugin.attributeHours and datetime_minute in regularPlugin.attributeMinutes:
					threading.Thread(name=regularPlugin.attributeName, target=_do, args=(regularPlugin, )).start()
			time.sleep(1)

	def __watchThreadActivity(self):
		while True:
			result = [thread.name for thread in threading.enumerate()]
			json.dump(result, open(jsonDir + "/thread.json", "w"), sort_keys=True)
			# db['Set'].update_one({}, {"$set": {"threadc": len(result)}})

			for threadPlugin in self.plugins[pluginThread]:
				if threadPlugin.attributeName not in result:
					t = threadPlugin.do()
					t.setName(threadPlugin.attributeName)
					t.start()

			time.sleep(15)

	def __newPluginFound(self, pluginPath):
		self.PM.addPlugin(pluginPath)

	def __pluginDeleted(self, pluginPath):
		self.PM.deletePlugin(pluginPath)

	class ChangeHandler(RegexMatchingEventHandler):
		def __init__(self, regexes):
			super(RegexMatchingEventHandler, self).__init__()
			self._regexes = [re.compile(r) for r in regexes]
			self.

		def on_created(self, event):
			pluginPath = event.src_path
			self.PM.addPlugin(pluginPath)

		def on_modified(self, event):
			pluginPath = event.src_path
			self.PM.addPlugin(pluginPath)

		def on_deleted(self, event):
			pluginPath = event.src_path
			self.PM.deletePlugin(pluginPath)
