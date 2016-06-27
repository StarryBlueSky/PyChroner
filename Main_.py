#! python3
# -*- coding: utf-8 -*-
import datetime
import gc
import json
import os
import random
import re
import socket
import subprocess
import sys
import threading
import time
import traceback
import urllib
from importlib import machinery
from logging import getLogger, Formatter, FileHandler, INFO, CRITICAL

from pymongo import MongoClient
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import DBInfo
import Twitter
import tweepy

"""プラグインを初期化する関数"""
def InitializePlugins(init=True, newName=None):
	plugins = {}
	# PLUGIN_DIRから拡張機能読み込み
	pattern = re.compile('[^.].*\.py$')
	for plugin_file in os.listdir(PLUGIN_DIR):
		if pattern.match(plugin_file):
			name = plugin_file[:-3]
			try:
				loader = machinery.SourceFileLoader(name, PLUGIN_DIR + '/' + plugin_file)
				module = loader.load_module(name)
				module.NAME = name
				if not hasattr(module, 'PRIORITY'):
					module.PRIORITY = 0
				if not hasattr(module, 'STREAM'):
					module.STREAM = 0
				usedStream.append(module.STREAM)
				plugins[name] = module
				if newName == name:
					logger.info('プラグイン「%s」(%s/%s)は有効になりました。' % (name, PLUGIN_DIR, plugin_file))
			except Exception as e:
				if newName == name:
					logger.warning('プラグイン「%s」(%s/%s)は有効にできませんでした。\nエラーログ: %s' % (name, PLUGIN_DIR, plugin_file, e))
	# プラグインの種類を分類
	if init == False:
		global reply_plugin, timeline_plugin, event_plugin, thread_plugin, regular_plugin, other_plugin
		reply_plugin, timeline_plugin, event_plugin, thread_plugin, regular_plugin, other_plugin = [], [], [], [], [], []
	# プラグインを優先順位に並べる
	plugins = sorted(plugins.items(), key=lambda x:x[1].PRIORITY, reverse=True)
	# プラグインの種類を分類
	for i in plugins:
		plugin = i[1]
		if plugin.TARGET == 'REPLY':
			reply_plugin.append(plugin)
		elif plugin.TARGET == 'TIMELINE':
			timeline_plugin.append(plugin)
		elif plugin.TARGET == 'EVENT':
			event_plugin.append(plugin)
		elif plugin.TARGET == 'THREAD':
			thread_plugin.append(plugin)
		elif plugin.TARGET == 'REGULAR':
			regular_plugin.append(plugin)
		elif plugin.TARGET == 'OTHER':
			other_plugin.append(plugin)

"""UserStreamを処理する関数"""
def StreamLine(raw, n, sn):
	stream = json.loads(raw)
	try:
		if 'text' in stream or 'direct_message' in stream:
			#記録
			db['Set'].update_one({}, {"$inc": {"minly_tweet": 1}})

			#DMを扱えるように変換
			if 'direct_message' in stream:
				stream = stream['direct_message']
				stream['user'] = stream['sender']
				stream['DM'] = True
				stream['source'] = ''
				stream['text'] = '@'+Set['twitterSecret'][0]['screen_name']+' '+stream['text']

			#管理者アカウント
			if stream['user']['screen_name'] in Set['account']['admin']:
				if 'execute_as' in stream['text']:
					tmp = stream['text'].split(' ')
					exer = stream['user']['screen_name']
					stream['text'] = tmp[0] + ' ' + ' '.join(tmp[3:])
					stream['user']['id'] = Twitter.tryAPI('get_user', 'screen_name="'+tmp[2]+'"').id
					stream['user']['screen_name'] = tmp[2]
					stream["DM"] = True
					stream["exer"] = exer
				elif 'repeat' in stream['text']:
					tmp = stream['text'].split(' ')
					n = int(tmp[2])
					text = tmp[0] + ' ' + ' '.join(tmp[3:])
					stream['text'] = text
					i = 1
					if n> 5:
						n = 5
					while i <= n:
						threading.Thread(target=StreamLine, name='StreamLine', args=(json.dumps(stream), )).start()
						i += 1
			#めかぞらる自身のツイートである
			if stream['user']['screen_name'] == SN:
				if not '@' in stream['text']:
					if random.randint(0, 50) == 0:
						db['Set'].update_one({}, {"$set": {"recentlyTweet": []}})
					db['Set'].update_one({}, {"$push": {"recentlyTweet": stream['text']}})
				elif not stream['text'].startswith('RT @'):
					if random.randint(0, 50) == 0:
						db['Set'].update_one({}, {"$set": {"recentlyReply": []}})
					db['Set'].update_one({}, {"$push": {"recentlyReply": stream['text']}})
				if re.match('(%s)' % '|'.join(Set['NGWord']), stream['text']):
					Twitter.Post(text='失礼しました', stream=stream, tweetid=stream['id'])
				return True
			#スパムを除去
			stream['source'] = re.sub('<.*?>','', stream['source'])
			domain = None
			if len(stream['entities']['urls']) > 0:
				domain = re.sub('http.*?\/\/(.*?)\/.*$', r'\1', stream['entities']['urls'][0]['expanded_url'])
			if stream['user']['screen_name'] in Set['ban']['screen_name'] or stream['source'] in Set['ban']['client'] or domain in Set['ban']['domain']:
				return True
			#RTは処理しない
			if stream['text'].startswith('RT @'):
				return True
			#名前欄攻撃対策(@リプ爆撃防止)
			stream['user']['name'] = stream['user']['name'].replace('@', '@​')
			#スペースや改行を整形
			stream['text'] = stream['text'].replace('\n', ' ')
			stream['text'] = stream['text'].replace('　', ' ')
			stream['text'] = stream['text'].replace('  ', ' ')

			if re.match('@%s\s' % SN, stream['text'], re.IGNORECASE):
				for plugin in reply_plugin:
					if plugin.STREAM == n:
						ExecutePlugin(plugin, stream)

			for plugin in timeline_plugin:
				if plugin.STREAM == n:
					ExecutePlugin(plugin, stream)

		elif 'event' in stream:
			db['Set'].update_one({}, {"$inc": {"minly_event": 1}})
			for plugin in event_plugin:
				if plugin.STREAM == n:
					ExecutePlugin(plugin, stream)

		else:
			for plugin in other_plugin:
				if plugin.STREAM == n:
					ExecutePlugin(plugin, stream)

	except Exception:
		logger.warning('UserStream(%s, %s)でエラーが発生しました\n詳細: %s' % (n, sn, traceback.format_exc()))

"""プラグインを実行する関数"""
def ExecutePlugin(plugin, stream):
	try:
		if 'RATIO' in dir(plugin):
			ratio = plugin.RATIO
		else:
			ratio = 1
		if random.randint(1, ratio) == 1: # 1/RATIOの確率でプラグイン実行
			if plugin.do.__code__.co_argcount == 2:
				if plugin.STREAM != 0:
					n = plugin.STREAM
					auth = tweepy.OAuthHandler(Set['twitterSecret'][n]['ck'], Set['twitterSecret'][n]['cs'])
					auth.set_access_token(Set['twitterSecret'][n]['at'], Set['twitterSecret'][n]['ats'])
					api = tweepy.API(auth)
				else:
					api = API
				# 引数の数が2の場合、グローバル変数を渡す
				result = plugin.do(stream, MakeArgsDic(api))
			else:
				result = plugin.do(stream)

	except Exception as e:
		logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, traceback.format_exc()))
		if plugin.TARGET == 'REPLY': # リプライプラグインの時のみユーザーにエラーを知らせる
			text = '@%s プラグイン "%s"でエラーが発生しました。\n\n詳細: %s' % (stream['user']['screen_name'], plugin.NAME, e[0:20])
			Twitter.Post(text, stream)

def MakeArgsDic(api=None):
	if api == None:
		api = API
	gvars = {
		"set": db['Set'].find_one(),
		"logger": logger,
		"api": api,
		"db": db,
		"auth": auth,
		"path": {
			"plugin_dir": PLUGIN_DIR,
			"data_dir": DATA_DIR
		},
		"plugin": {
			"reply": reply_plugin,
			"timeline": timeline_plugin,
			"event": event_plugin,
			"thread": thread_plugin,
			"regular": regular_plugin
		}
	}
	return gvars

def MakeUserStreamConnection(n):
	auth = tweepy.OAuthHandler(Set['twitterSecret'][n]['ck'], Set['twitterSecret'][n]['cs'])
	auth.set_access_token(Set['twitterSecret'][n]['at'], Set['twitterSecret'][n]['ats'])
	sn = Set['twitterSecret'][n]['screen_name']
	while True:
		try:
			logger.info('@%sのUserStreamに接続しました。' % sn)
			UserStream(auth, StreamListener(n, sn)).user_stream()
		except Exception as e:
			logger.warning('UserStreamから切断されました。10秒後に再接続します。エラーログ: %s' % traceback.format_exc())
			time.sleep(10)

"""tweepyのクラスを継承してUserStreamを受信するクラス"""
class StreamListener(tweepy.StreamListener):
	def __init__(self, n, sn):
		self.n = n
		self.sn = sn

	def on_data(self, raw):
		if raw.startswith('{'):
			t = threading.Thread(target=StreamLine, name='StreamLine', args=(raw, self.n, self.sn))
			t.start()
			return True
		else:
			logger.warning('解析不能なUserStreamデータを受信しました: %s' % raw)
			return False

	def on_error(self, status_code):
		logger.warning('Twitter APIエラーが発生しました\n詳細: HTTPステータスコード=%s' % status_code)

"""tweepyのクラスを継承してUserStreamの設定をするクラス"""
class UserStream(tweepy.Stream):
	def user_stream(self):
		self.parameters = {"delimited": "length", "replies": "all", "filter_level": "none", "include_followings_activity": "True", "stall_warnings": "True", "with": "followings"}
		self.headers['Content-type'] = "application/x-www-form-urlencoded"
		self.scheme = "https"
		self.host = 'userstream.twitter.com'
		self.url = '/1.1/user.json'
		self.body = urllib.parse.urlencode(self.parameters)
		self.timeout = None
		self._start(False)

"""定期実行プラグインを実行するクラス"""
class ScheduleTask(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			def do(plugin):
				def _do():
					try:
						if plugin.do.__code__.co_argcount == 1:
							# 引数の数が1の場合、グローバル変数を渡す
							plugin.do(MakeArgsDic())
						else:
							plugin.do()
						logger.info('定期実行プラグイン「%s」を実行しました。' % plugin.NAME)
					except:
						logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, traceback.format_exc()))
				threading.Thread(name=plugin.NAME, target=_do).start()
			wait_time = 60 - datetime.datetime.now().second
			time.sleep(wait_time)
			datetime_hour = datetime.datetime.now().hour
			datetime_minute = datetime.datetime.now().minute
			for plugin in regular_plugin:
				if 'RATIO' in dir(plugin):
					ratio = plugin.RATIO
				else:
					ratio = 1
				if random.randint(1, ratio) != 1: # 1/RATIOの確率でプラグイン実行
					continue

				if 'HOUR' in dir(plugin):
					if not isinstance(plugin.HOUR, list):
						hour = [plugin.HOUR]
					else:
						hour = plugin.HOUR
				else:
					hour = None
				if 'MINUTE' in dir(plugin):
					if not isinstance(plugin.MINUTE, list):
						minute = [plugin.MINUTE]
					else:
						minute = plugin.MINUTE
				else:
					minute = None
				if hour != None and minute != None:
					if datetime_hour in hour and datetime_minute in minute: # 時と分指定型
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif hour != None:
					if datetime_hour in hour: # 時だけ指定型(その時だけ毎分実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif minute != None:
					if datetime_minute in minute: # 分だけ指定型(その分だけ毎時実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				# ある倍数の時だけ実行する
				if 'MULTIPLE_HOUR' in dir(plugin):
					multiple_hour = plugin.MULTIPLE_HOUR
				else:
					multiple_hour = None
				if 'MULTIPLE_MINUTE' in dir(plugin):
					multiple_minute = plugin.MULTIPLE_MINUTE
				else:
					multiple_minute = None
				if multiple_hour != None and multiple_minute != None:
					if datetime_hour % multiple_hour == 0 and datetime_minute % multiple_minute == 0: # 時と分の倍数指定型
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif multiple_hour != None:
					if datetime_hour % multiple_hour == 0 and datetime_minute == 0: # 時だけ倍数指定型(その倍数時だけ毎分実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif multiple_minute != None:
					if datetime_minute % multiple_minute == 0: # 分だけ倍数指定型(その倍数分だけ毎時実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
			time.sleep(1)

"""スレッドを監視するクラス"""
class CheckThreading(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		result = [x.name for x in threading.enumerate()]
		dic = {}
		dic['threads'] = result
		json.dump(dic, open(Set['path']['base'] + Set['path']['data'] + '/json/thread.json', 'w'), sort_keys=True)
		for x in thread_plugin:
			if not x.NAME in result:
				t = x.do()
				t.setName(x.NAME)
				t.start()
		db['Set'].update_one({}, {"$set": {"threadc": threading.active_count()}})
		time.sleep(15)

"""プラグインディレクトリを監視するハンドラ"""
class ChangeHandler(FileSystemEventHandler):
	def on_created(self, event):
		if event.is_directory:
			return
		if not event.src_path.endswith('.py'):
			return
		name = event.src_path[:-3].replace(PLUGIN_DIR+'/', '')
		try:
			loader = machinery.SourceFileLoader(name, event.src_path)
			module = loader.load_module(name)
			module.NAME = name
			if module.TARGET == 'REPLY':
				reply_plugin.append(module)
			elif module.TARGET == 'TIMELINE':
				timeline_plugin.append(module)
			elif module.TARGET == 'EVENT':
				event_plugin.append(module)
			elif module.TARGET == 'THREAD':
				thread_plugin.append(module)
			elif module.TARGET == 'REGULAR':
				regular_plugin.append(module)
			elif module.TARGET == 'OTHER':
				other_plugin.append(module)
			logger.info('プラグイン「%s」は有効になりました。' % name)
		except Exception as e:
			logger.warning('プラグイン「%s」は壊れています。有効にできませんでした。\nエラーログ: %s' % (name, e))

	def on_modified(self, event):
		if event.is_directory:
			return
		if not event.src_path.endswith('.py'):
			return
		InitializePlugins(init=False, newName=event.src_path[:-3].replace(PLUGIN_DIR+'/', ''))

	def on_deleted(self, event):
		if event.is_directory:
			return
		if not event.src_path.endswith('.py'):
			return
		InitializePlugins(init=False, newName=event.src_path[:-3].replace(PLUGIN_DIR+'/', ''))

if __name__ == '__main__':
	"""データベースに接続"""
	connect = MongoClient(DBInfo.Host)
	global  db
	db = connect.bot
	db.authenticate(DBInfo.Username, DBInfo.Password, mechanism=DBInfo.Method)
	global Set
	Set = db['Set'].find_one()
	
	"""引数モード"""
	param = sys.argv
	if len(param) == 1:
		sys.exit()
	# デーモンモード
	elif param[1] == 'daemon':
		subprocess.run('python3 %sMain.py run &> %s%s/stdout.log &' \
			% (Set['path']['base'], Set['path']['base'], Set['path']['log']), shell=True)

	# アカウント確認モード
	elif param[1] == 'check':
		pass
		# CheckIfAccountIsAlive(output=True, reboot=False)

	elif param[1] == 'eval':
		stream = {"text": param[3].replace('+', ' '), "id": int(param[2]), "source": "<a href='https://app.zoraru.info/run'>めかぞらる仮想コンソール</a>", "user":{"id": 0, "screen_name": "WEB_CONSOLE", "name": "めかぞらる Web 仮想コンソール"}, "entities": {"urls": []}}
		print(stream)
		print((StreamLine(json.dumps(stream))))

	# スタンドアロンモード
	elif param[1] == 'run': 
		# プロセス個数確認
		if subprocess.getoutput('ps ax | grep Main.py\ run | grep -v grep') == '':
			sys.exit()
		""""パスを読み込み"""
		global  PLUGIN_DIR, DATA_DIR
		PLUGIN_DIR = Set['path']['base'] + Set['path']['plugin']
		DATA_DIR = Set['path']['base'] + Set['path']['data']
		# ディレクトリがない場合は生成
		if not os.path.isdir(PLUGIN_DIR):
			os.makedirs(PLUGIN_DIR)
		if not os.path.isdir(DATA_DIR):
			os.makedirs(DATA_DIR)
	
		"""ロガーを準備"""
		handler = FileHandler(Set['path']['base'] + Set['path']['log']+'/logger/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log', 'w', encoding='utf-8')
		formatter = Formatter('[%(levelname)s]%(asctime)s - %(message)s')
		handler.setFormatter(formatter)
		getLogger("requests").setLevel(CRITICAL)
		getLogger("tweepy").setLevel(CRITICAL)
		global logger
		logger = getLogger()
		logger.addHandler(handler)
		logger.setLevel(INFO)

		"""プラグインを格納するリストを定義"""
		global reply_plugin, timeline_plugin, event_plugin, thread_plugin, regular_plugin, other_plugin
		reply_plugin = []
		timeline_plugin = []
		event_plugin = []
		thread_plugin = []
		regular_plugin = []
		other_plugin = []
		global usedStream
		usedStream = []

		""""初期化"""
		gc.enable()
		boottime = datetime.datetime.now()
		logger.info('現在の時刻は %s です。' % boottime)
		logger.info('アカウントの可用性を確認しています。')
		result = subprocess.run('python3 %sMain.py check' % Set['path']['base'], shell=True)
		logger.info('初期化に成功しました。')

		db['Set'].update_one({}, {"$set": {"lastrun": datetime.datetime.now()}})
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
		opener.addheaders=[('User-Agent', Set['useragent']['service']),('Accept-Language', Set['acceptlanguage'])]
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
			t = threading.Thread(name='Streaming for %s' % n, target=MakeUserStreamConnection, args=(n, ))
			t.start()
		while True:
			time.sleep(100)
