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
from logging import getLogger, captureWarnings, Formatter, INFO, CRITICAL
from logging.handlers import RotatingFileHandler

import tweepy
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer

from TBFW.configparser import ConfigParser
from TBFW.constant import *
from TBFW.plugin import PluginManager
from TBFW.twitterapi import TwitterAPI, UserStream


class _Core:
	def __init__(self):
		gc.enable()
		socket.setdefaulttimeout(30)

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-Agent', userAgent), ('Accept-Language', acceptLanguage)]
		urllib.request.install_opener(opener)

		for directory in dirs:
			if not os.path.isdir(directory):
				os.mkdir(directory)

		self.PM = PluginManager()
		self.PM.searchAllPlugins()
		self.plugins = self.PM.plugins
		self.attachedStreamId = self.PM.attachedStreamId

		self.logPath = logDir + "/" + datetime.now().strftime(messageLogDatetimeFormat) + ".log"
		self.__logger = self.__getLogger()

		self.boottime = datetime.now()
		self.__logger.info(messageSuccessInitialization.format(self.boottime))

	def __getLogger(self):
		logger = getLogger()
		captureWarnings(capture=True)

		handler = RotatingFileHandler(self.logPath, maxBytes=20, encoding="utf-8")
		formatter = Formatter(messageLogFormat, messageLogTimeFormat)
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
		observer.schedule(ChangeHandler(regexes=["\.py$"]), pluginsDir, recursive=False)
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
			for currentRegularPlugin in self.plugins[pluginRegular]:
				if random.randint(1, currentRegularPlugin.attributeRatio) != 1:
					continue
				if datetime_hour in currentRegularPlugin.attributeHours and datetime_minute in currentRegularPlugin.attributeMinutes:
					threading.Thread(name=currentRegularPlugin.attributeName, target=_do, args=(currentRegularPlugin, )).start()
			time.sleep(1)

	def __watchThreadActivity(self):
		while True:
			result = [thread.name for thread in threading.enumerate()]
			json.dump(result, open(apiDir + "/" + pathThreadApi, "w"), sort_keys=True)

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
__Config = ConfigParser()
accounts = __Config.accounts
muteClient = __Config.muteClient
muteUser = __Config.muteUser
muteDomain = __Config.muteDomain

class Streaming:
	def __init__(self, sn, streamId):
		self.sn = sn
		self.streamId = streamId

		self.__ck = accounts[streamId]["ck"]
		self.__cs = accounts[streamId]["cs"]
		self.__at = accounts[streamId]["at"]
		self.__ats = accounts[streamId]["ats"]

		self.__logger = getLogger(__name__)

	def startUserStream(self):
		auth = tweepy.OAuthHandler(self.__ck, self.__cs)
		auth.set_access_token(self.__at, self.__ats)

		while True:
			try:
				self.__logger.info('@%sのUserStreamに接続しました。' % self.sn)
				UserStream(auth, StreamListener(self.sn, self.streamId)).user_stream()
			except:
				self.__logger.warning('@%sのUserStreamから切断されました。10秒後に再接続します。エラーログ: \n%s' % (self.sn, traceback.format_exc()))
				time.sleep(reconnectUserStreamSeconds)

	def _processStream(self, rawJson):
		stream = json.loads(rawJson)
		try:
			if "text" in stream:
				via = re.sub("<.*?>", "", stream['source'])
				if stream['user']['screen_name'] in muteUser or via in muteClient:
					return
				if len(stream['entities']['urls']) > 0:
					domain = re.sub('http(|s)://(.+?)/.*$', '\1', stream['entities']['urls'][0]['expanded_url'])
					if domain in muteDomain:
						return

				stream['user']['name'] = stream['user']['name'].replace("@", "@​")

				if re.match('@%s\s' % self.sn, stream['text'], re.IGNORECASE):
					for plugin in Core.plugins[pluginReply]:
						if getattr(plugin, pluginAttributeAttachedStream) == self.streamId:
							self.__executePlugin(plugin, stream)
							break
				for plugin in Core.plugins[pluginTimeline]:
					if getattr(plugin, pluginAttributeAttachedStream) == self.streamId:
						self.__executePlugin(plugin, stream)

			elif 'event' in stream:
				for plugin in Core.plugins[pluginEvent]:
					if getattr(plugin, pluginAttributeAttachedStream) == self.streamId:
						self.__executePlugin(plugin, stream)

			else:
				for plugin in Core.plugins["other"]:
					if plugin.STREAM == self.streamId:
						self.__executePlugin(plugin, stream)

		except Exception:
			self.__logger.exception(messageErrorProcessingStream.format(self.sn))

	def __executePlugin(self, plugin, stream):
		try:
			if random.randint(1, plugin.attributeRatio) == 1:
				plugin.code.do(stream)

		except Exception as e:
			self.__logger.exception(messageErrorExecutingPlugin.format(plugin.attributeName))
			if plugin.attributeTarger == 'REPLY' and "@" + self.sn in stream['text']:
				text = messageTweetErrorExecutingPlugin.format(self.sn, plugin.attributeName, e[0:20])
				API = TwitterAPI(accountId=self.streamId)
				Twitter.Post(text, stream=stream, tweetid=stream['id'])

class StreamListener(tweepy.StreamListener):
	def __init__(self, sn, streamId):
		self.sn = sn
		self.streamId = streamId
		self.__logger = getLogger(__name__)

	def on_data(self, rawJson):
		streaming = Streaming(self.sn, self.streamId)
		t = threading.Thread(target=streaming._processStream, name="_processStream", args=(rawJson, ))
		t.start()

	def on_error(self, status_code):
		self.__logger.warning(messageErrorConnectingTwitter.format(status_code))

class ChangeHandler(RegexMatchingEventHandler):
	def __init__(self, regexes):
		super(RegexMatchingEventHandler, self).__init__()
		self._regexes = [re.compile(r) for r in regexes]

	def on_created(self, event):
		pluginPath = event.src_path
		Core._newPluginFound(pluginPath)

	def on_modified(self, event):
		pluginPath = event.src_path
		Core._newPluginFound(pluginPath)

	def on_deleted(self, event):
		pluginPath = event.src_path
		Core._pluginDeleted(pluginPath)
