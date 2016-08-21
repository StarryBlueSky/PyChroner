# coding=utf-8
import gc
import json
import random
import re
import socket
import threading
import time
import traceback
import urllib
import urllib.parse
from datetime import datetime
from logging import getLogger, captureWarnings, Formatter, INFO, CRITICAL
from logging.handlers import RotatingFileHandler

from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer

from TBFW.constant import *
from TBFW.plugin import PluginManager
from TBFW.twitterapi import TwitterAPI

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

		self.TwitterAPI = TwitterAPI()

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
			for regularPlugin in self.plugins["regular"]:
				if random.randint(1, regularPlugin.attributeRatio) != 1:
					continue
				if datetime_hour in regularPlugin.attributeHours and datetime_minute in regularPlugin.attributeMinutes:
					threading.Thread(name=regularPlugin.attributeName, target=_do, args=(regularPlugin, )).start()
			time.sleep(1)

	def __watchThreadActivity(self):
		while True:
			result = [thread.name for thread in threading.enumerate()]
			json.dump(result, open(apiDir + "/thread.json", "w"), sort_keys=True)
			# db['Set'].update_one({}, {"$set": {"threadc": len(result)}})

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

def StreamLine(raw, n, sn):
	stream = json.loads(raw)
	try:
		if 'text' in stream:
			# 禁止ユーザーとクライアントを拒否
			stream['source'] = re.sub('<.*?>', '', stream['source'])
			if stream['user']['screen_name'] in Set['ban']['screen_name'] or stream['source'] in Set['ban']['client']:
				return
			# RTは処理しない
			if stream['text'].startswith('RT @'):
				return
			# URLスパムを除去
			if len(stream['entities']['urls']) > 0:
				domain = re.sub('http.*?\/\/(.*?)\/.*$', r'\1', stream['entities']['urls'][0]['expanded_url'])
				if domain in Set['ban']['domain']:
					return
			# 名前欄攻撃対策(@リプ爆撃防止)
			stream['user']['name'] = stream['user']['name'].replace('@', '@​')
			# スペースや改行を整形
			stream['text'] = stream['text'].replace('\n', ' ')
			stream['text'] = stream['text'].replace('　', ' ')
			stream['text'] = stream['text'].replace('  ', ' ')

			if re.match('@%s\s' % sn, stream['text'], re.IGNORECASE):
				for plugin in plugins["reply"]:
					if plugin.STREAM == n:
						ExecutePlugin(plugin, stream)
						break
			for plugin in plugins["timeline"]:
				if plugin.STREAM == n:
					ExecutePlugin(plugin, stream)

		elif 'event' in stream:
			for plugin in plugins["event"]:
				if plugin.STREAM == n:
					ExecutePlugin(plugin, stream)

		else:
			for plugin in plugins["other"]:
				if plugin.STREAM == n:
					ExecutePlugin(plugin, stream)

	except Exception:
		logger.warning('UserStream(%s, %s)でエラーが発生しました。\n詳細: %s' % (n, sn, traceback.format_exc()))

"""プラグインを実行する関数"""
def ExecutePlugin(plugin, stream):
	try:
		if random.randint(1, plugin.RATIO) == 1:  # 1/RATIOの確率でプラグイン実行
			if plugin.do.__code__.co_argcount == 2:
				# 引数の数が2の場合、グローバル変数を渡す
				plugin.do(stream, MakeArgsDic())
			else:
				plugin.do(stream)

	except Exception as e:
		CommonUtil.Report()
		if plugin.TARGET == 'REPLY' and "@" + Set['twitterSecret'][0]['screen_name'] in stream['text']:
			# リプライプラグインの時のみユーザーにエラーを知らせる
			text = '@%s プラグイン "%s"でエラーが発生しました。申し訳ありませんが、しばらく経ってから再試行してください。問題が解決しない場合には、製作者までお問い合わせ下さい。\n\n詳細: %s' % (stream['user']['screen_name'], plugin._NAME, e[0:20])
			Twitter.Post(text, stream=stream, tweetid=stream['id'])

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
