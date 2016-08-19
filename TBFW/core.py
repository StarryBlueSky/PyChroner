# coding=utf-8
import os
import gc
from datetime import datetime
from TBFW.constant import *
from logging import getLogger, Formatter, FileHandler, INFO, CRITICAL

class Core:
	def __init__(self):
		gc.enable()

		self.currentDir = os.getcwd()
		self.pluginsDir = self.currentDir + "/" + pathPluginsDir
		self.logDir = self.currentDir + "/" + pathLogDir

		for directory in [self.pluginsDir, self.logDir]:
			if not os.path.isdir(directory):
				os.mkdir(directory)

		self.logPath = self.logDir + "/" + datetime.now().strftime(messageLogDatetimeFormat) + ".log"
		self.logger = self.getLogger()

		self.boottime = datetime.now()
		self.logger.info(messageSuccessInitialization.format(self.boottime))

	def getLogger(self):
		logger = getLogger()
		handler = FileHandler(self.logPath, "w", encoding="utf-8")
		formatter = Formatter(messageLogFormat)
		handler.setFormatter(formatter)

		getLogger("requests").setLevel(CRITICAL)
		getLogger("tweepy").setLevel(CRITICAL)

		logger.addHandler(handler)
		logger.setLevel(INFO)

		return logger

	def Start(self):
		db['Set'].update_one({}, {"$set": {"lastrun": datetime.now()}})
		db['Set'].update_one({}, {"$set": {"timed": 0, "threadc": 1, "minly": {"tweet": 0, "event": 0}}})
		Set = db['Set'].find_one()

		# UserStreamに接続するアカウントの認証
		auth = tweepy.OAuthHandler(Set['twitterSecret'][0]['ck'], Set['twitterSecret'][0]['cs'])
		auth.set_access_token(Set['twitterSecret'][0]['at'], Set['twitterSecret'][0]['ats'])
		global API
		API = tweepy.API(auth)
		SN = Set['twitterSecret'][0]['screen_name']

		# UserAgentの定義
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-Agent', Set['useragent']['service']), ('Accept-Language', Set['acceptlanguage'])]
		urllib.request.install_opener(opener)
		# タイムアウトの定義
		socket.setdefaulttimeout(30)

		# プラグイン読み込み
		InitializePlugins()

		"""別スレッドで処理するスレッドを起動"""
		for x in thread_plugin:
			t = x.do()
			t.setName(x.NAME)
			t.start()
		ScheduleTask().start()
		CheckThreading().start()

		""""プラグインディレクトリを監視"""
		event_handler = ChangeHandler()
		observer = Observer()
		observer.schedule(event_handler, PLUGIN_DIR, recursive=False)
		observer.start()

		"""UserStreamに接続"""
		usedStream = list(set(usedStream))
		for n in usedStream:
			t = threading.Thread(name='Streaming for %s' % n, target=MakeUserStreamConnection, args=(n,))
			t.start()
		while True:
			time.sleep(100)
