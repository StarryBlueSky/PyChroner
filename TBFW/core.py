# coding=utf-8
import gc
import json
import random
import re
import socket
import threading
import time
import traceback
import urllib.parse
from datetime import datetime
from logging import getLogger, captureWarnings, Formatter, DEBUG, INFO, CRITICAL
from logging.handlers import RotatingFileHandler

import tweepy
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from TBFW.configparser import ConfigParser
from TBFW.constant import *
from TBFW.plugin import PluginManager
from TBFW.twitterapi import TwitterOAuth, TwitterAPI, UserStream

configparser = ConfigParser()
config = configparser.config

class _Core:
	def __init__(self, debug=False):
		gc.enable()
		socket.setdefaulttimeout(30)

		opener = urllib.request.build_opener()
		opener.addheaders = [
			("User-Agent", userAgent),
			("Accept-Language", acceptLanguage)
		]
		urllib.request.install_opener(opener)

		for directory in dirs:
			if not os.path.isdir(directory):
				os.mkdir(directory)

		self.debug = debug
		self.logPath = logDir + "/" + datetime.now().strftime(messageLogDatetimeFormat) + ".log"
		self.__logger = self.__getLogger()

		self.PM = PluginManager()
		self.PM.searchAllPlugins()
		self.plugins = self.PM.plugins
		self.attachedAccountId = self.PM.attachedAccountId

		self.boottime = datetime.now()
		self.__logger.info(messageSuccessInitialization.format(self.boottime))

		for initializerPlugin in self.plugins[pluginInitializer]:
			initializerPlugin.code.do()

	def __getLogger(self):
		logger = getLogger()
		captureWarnings(capture=True)

		handler = RotatingFileHandler(self.logPath, maxBytes=2 ** 20, encoding="utf-8")
		formatter = Formatter(messageLogFormat, messageLogTimeFormat)
		handler.setFormatter(formatter)

		getLogger("requests").setLevel(CRITICAL)
		getLogger("tweepy").setLevel(CRITICAL)

		logger.setLevel(DEBUG if self.debug else INFO)
		logger.addHandler(handler)

		return logger

	def run(self):
		for threadPlugin in self.plugins[pluginThread]:
			t = threading.Thread(name=threadPlugin.attributeName, target=threadPlugin.code.do)
			t.start()
		threading.Thread(name="__scheduleRegularPlugins", target=self.__scheduleRegularPlugins).start()
		threading.Thread(name="__watchThreadActivity", target=self.__watchThreadActivity).start()

		observer = Observer()
		observer.schedule(ChangeHandler(), pluginsDir)
		observer.start()

		for accountId in self.attachedAccountId:
			streaming = Streaming(accountId)
			t = threading.Thread(name="Streaming_for_%s" % config.accounts[accountId].sn, target=streaming.startUserStream)
			t.start()

		while True:
			try:
				time.sleep(60)
			except KeyboardInterrupt:
				break

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
			for currentRegularPlugin in self.plugins[pluginRegular]:
				if random.randint(1, currentRegularPlugin.attributeRatio) != 1:
					continue
				if datetime_hour in currentRegularPlugin.attributeHours and datetime_minute in currentRegularPlugin.attributeMinutes:
					t = threading.Thread(name=currentRegularPlugin.attributeName, target=_do, args=(currentRegularPlugin, ))
					t.start()
			time.sleep(1)

	def __watchThreadActivity(self):
		while True:
			result = [thread.name for thread in threading.enumerate()]
			json.dump(result, open(apiDir + "/" + pathThreadApi, "w"), sort_keys=True, indent=4)

			for threadPlugin in self.plugins[pluginThread]:
				if threadPlugin.attributeName not in result:
					t = threadPlugin.do()
					t.setName(threadPlugin.attributeName)
					t.start()

			time.sleep(15)

	def _newPluginFound(self, pluginPath):
		self.PM.addPlugin(pluginPath)

	def _pluginDeleted(self, pluginPath):
		self.PM.deletePlugin(pluginPath)

Core = _Core()

class Streaming:
	def __init__(self, accountId):
		self.accountId = accountId

		self.accounts = config.accounts
		self.sn = self.accounts[accountId].sn

		self.__logger = getLogger(__name__)

		self.muteClient = config.muteClient
		self.muteUser = config.muteUser
		self.muteDomain = config.muteDomain

	def startUserStream(self):
		auth = TwitterOAuth(self.accountId)
		while True:
			try:
				self.__logger.info(messageSuccessConnectingUserStream.format(self.sn))
				UserStream(auth, StreamListener(self.accountId)).user_stream()
			except:
				self.__logger.exception(messageErrorConnectingUserStream.format(self.sn, reconnectUserStreamSeconds))
				time.sleep(reconnectUserStreamSeconds)

	def _processStream(self, rawJson):
		stream = json.loads(rawJson)
		try:
			if "direct_message" in stream:
				_stream = stream
				stream = stream["direct_message"]
				stream['user'] = stream["sender"]
				stream['source'] = ""
				stream["dm_obj"] = _stream
				stream['text'] = "@{0} {1}".format(self.sn, stream['text'])

			if "text" in stream:
				via = re.sub("<.*?>", "", stream['source'])
				if stream['user']['screen_name'] in self.muteUser or via in self.muteClient:
					return
				if len(stream['entities']['urls']) > 0:
					domain = re.sub("http(|s)://(.+?)/.*$", "\1", stream['entities']['urls'][0]['expanded_url'])
					if domain in self.muteDomain:
						return

				stream["user"]["name"] = stream["user"]["name"].replace("@", "@​")

				if re.match("@%s\s" % self.sn, stream["text"], re.IGNORECASE):
					for plugin in Core.plugins[pluginReply]:
						if plugin.attributeAttachedStream == self.accountId:
							self.__executePlugin(plugin, stream)
							break
					if "dm_obj" in stream:
						for plugin in Core.plugins[pluginDM]:
							if plugin.attributeAttachedStream == self.accountId:
								self.__executePlugin(plugin, stream)
								break
				for plugin in Core.plugins[pluginTimeline]:
					if plugin.attributeAttachedStream == self.accountId:
						self.__executePlugin(plugin, stream)

			elif "event" in stream:
				for plugin in Core.plugins[pluginEvent]:
					if plugin.attributeAttachedStream == self.accountId:
						self.__executePlugin(plugin, stream)

			else:
				for plugin in Core.plugins["other"]:
					if plugin.attributeAttachedStream == self.accountId:
						self.__executePlugin(plugin, stream)

		except Exception:
			self.__logger.exception(messageErrorProcessingStream.format(self.sn))

	def __executePlugin(self, plugin, stream):
		try:
			if random.randint(1, plugin.attributeRatio) == 1:
				plugin.code.do(stream)

		except Exception as e:
			self.__logger.exception(messageErrorExecutingPlugin.format(plugin.attributeName))
			if plugin.attributeTarger == "REPLY" and "@" + self.sn in stream["text"]:
				text = messageTweetErrorExecutingPlugin.format(self.sn, plugin.attributeName, e[0:20])
				API = TwitterAPI(accountId=self.accountId)
				API.update_status(text, in_reply_to_status_id=stream["id"])

class StreamListener(tweepy.StreamListener):
	def __init__(self, accountId):
		self.accountId = accountId
		self.__logger = getLogger(__name__)

	def on_data(self, rawJson):
		streaming = Streaming(self.accountId)
		t = threading.Thread(target=streaming._processStream, name="_processStream", args=(rawJson, ))
		t.start()

	def on_error(self, status_code):
		self.__logger.warning(messageErrorConnectingTwitter.format(status_code))

class ChangeHandler(FileSystemEventHandler):
	def on_created(self, event):
		if not event.src_path.endswith(".py"):
			return
		pluginPath = event.src_path
		Core._newPluginFound(pluginPath)

	def on_modified(self, event):
		if not event.src_path.endswith(".py"):
			return
		pluginPath = event.src_path
		Core._newPluginFound(pluginPath)

	def on_deleted(self, event):
		if not event.src_path.endswith(".py"):
			return
		pluginPath = event.src_path
		Core._pluginDeleted(pluginPath)
