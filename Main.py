#! python3
# -*- coding: utf-8 -*-
import re, urllib, json, threading, logging, random, os, datetime, time
from importlib import machinery
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import tweepy, yaml

"""プラグインを初期化する関数"""
def InitializePlugins(init=True):
	plugins = {}
	"""PLUGIN_DIRから拡張機能読み込み"""
	for plugin_file in os.listdir(PLUGIN_DIR):
		if re.compile('[^.].*\.py$').match(plugin_file):
			name = plugin_file[:-3]
			try:
				loader = machinery.SourceFileLoader(name, PLUGIN_DIR+'/'+name+'.py')
				module = loader.load_module(name)
				module.NAME = name
				plugins[name] = module
				logger.info('プラグイン「%s」は有効になりました。' % name)
				if module.do.__code__.co_argcount == 2:
					logger.info('プラグイン「%s」は`args`引数を要求しています。このプラグインが悪意のあるプラグインである場合、Twitterアカウントを乗っ取られたりキャッシュが破壊されたりする可能性があります。ご注意ください。' % name)
			except Exception as e:
				logger.warning('プラグイン「%s」は壊れています。有効にできませんでした。\nエラーログ: %s' % (name, e))
	"""pluginの種類を分類"""
	if init == False:
		global reply_plugin, timeline_plugin, event_plugin, thread_plugin, regular_plugin
		reply_plugin, timeline_plugin, event_plugin, thread_plugin, regular_plugin = [], [], [], [], []
	for i in plugins:
		plugin = plugins[i]
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

"""プラグインの結果をツイートする関数"""
def Post(text, stream, dm=False, lat=None, longs=None, in_reply_to_status_id=None, filename=None):
	try:
		if dm == True:
			API.send_direct_message(screen_name=stream['user']['screen_name'], text=text)
		elif filename == None:
			API.update_status(status=text, in_reply_to_status_id=in_reply_to_status_id, lat=lat, int=longs)
		else:
			API.update_with_media(filename=filename, status=text, in_reply_to_status_id=in_reply_to_status_id, lat=lat, int=longs)
		return True
	except tweepy.TweepError as e:
		code = e[0]
		if code == 186: # 186 = Status is over 140 characters
			Post('@%s ツイートが長すぎるため、DMで送信しました。' % stream['user']['screen_name'], stream, dm=False, lat=lat, longs=longs, in_reply_to_status_id=in_reply_to_status_id, filename=filename)
			Post(text, stream, dm=True, lat=lat, longs=longs, in_reply_to_status_id=in_reply_to_status_id, filename=filename)
			return True
		elif code in [150, 187, 226]:
			logger.warning('Twitter APIエラーが発生しました\n詳細: %s' % ' '.join(e))
			#150 = only you can send messages to who follows you(DM)
			#187 = Status is a duplicate
			#226 = your request was automated
		elif code == 354:
			#354 = too long message(DM)
			return False

"""UserStreamを処理する関数"""
def StreamLine(raw):
	stream = json.loads(raw)
	try:
		if 'text' in stream:
			stream['source'] = re.sub('<.*?>','', stream['source'])
			#名前欄攻撃対策(@リプ爆撃防止)
			stream['user']['name'] = stream['user']['name'].replace('@', '@​')
			#スペースや改行を整形
#			stream['text'] = stream['text'].replace('\n', ' ')
#			stream['text'] = stream['text'].replace('　', ' ')
#			stream['text'] = stream['text'].replace('  ', ' ')

			if re.match('@%s\s' % SN, stream['text'], re.IGNORECASE):
				for plugin in reply_plugin:
					ExecutePlugin(plugin, stream)

			for plugin in timeline_plugin:
				ExecutePlugin(plugin, stream)

		elif 'event' in stream:
			for plugin in event_plugin:
				ExecutePlugin(plugin, stream)

	except Exception as e:
		logger.warning('UserStreamでエラーが発生しました\n詳細: %s' % ' '.join(e))

"""プラグインを実行する関数"""
def ExecutePlugin(plugin, stream):
	try:
		if 'RATIO' in dir(plugin):
			ratio = plugin.RATIO
		else:
			ratio = 1
		if random.randint(1, ratio) == 1: #1/RATIOの確率でプラグイン実行
			if plugin.do.__code__.co_argcount == 2:
				#引数の数が2の場合、グローバル変数を渡す
				gvars = {"setting": setting,
								"logger": logger,
								"api": API,
								"auth": auth,
								"cache": CACHE,
								"path": {"script": __file__, "plugin_dir": PLUGIN_DIR, "cache": CACHE_PARH, "setting": SETTING_PATH, "work_dir": WORK_DIR, "log": LOG_PATH},
								"plugin": {"reply": reply_plugin, "timeline": timeline_plugin, "event": event_plugin, "thread": thread_plugin, "regular": regular_plugin}
								}
				result = plugin.do(stream, gvars)
			else:
				result = plugin.do(stream)
		else: #そうでなければ終了
			return True
		if result:
			if isinstance(result, dict):
				if 'text' in result:
					text = result['text']
					if 'dm' in result: dm = result['dm']
					else: dm = False
					if 'lat' in result: lat = result['lat']
					else: lat = None
					if 'longs' in result: longs = result['longs']
					else: longs = None
					if 'in_reply_to_status_id' in result: in_reply_to_status_id = result['in_reply_to_status_id']
					else: in_reply_to_status_id = None
					if 'filename' in result: filename = result['filename']
					else: filename = None
					Post(text, stream, dm, lat, longs, in_reply_to_status_id, filename)
				if 'update' in result:
					#updateの中身を統合
					CACHE.update(result['update'])
		elif result == False:
			raise Exception
	except Exception as e:
		if plugin.TARGET == 'REPLY': #リプライプラグインの時のみユーザーにエラーを知らせる
			text = '@%s プラグイン "%s"でエラーが発生しました。\n\n詳細: %s' % (stream['user']['screen_name'], plugin.NAME, e)
			Post(text, stream)
		logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))

"""キャッシュを保存する関数"""
def SaveCache():
	open(CACHE_PARH, 'w').write(str(CACHE))

"""tweepyのクラスを継承してUserStreamを受信するクラス"""
class StreamListener(tweepy.StreamListener):
	def on_data(self, raw):
		if raw.startswith('{'):
			t = threading.Thread(target=StreamLine, name='StreamLine', args=(raw, ))
			t.start()
			t.join(20) #スレッドのタイムアウト 20秒
			if t.isAlive():
				t.__stop()
				logger.warning('スレッドがタイムアウトしました: %s' % raw)
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

"""定期実行するプラグインを実行するクラス"""
class ScheduleTask(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			def do(plugin):
				if plugin.do.__code__.co_argcount == 1:
					#引数の数が1の場合、グローバル変数を渡す
					gvars = {"setting": setting,
								"logger": logger,
								"api": API,
								"auth": auth,
								"cache": CACHE,
								"path": {"script": __file__, "plugin_dir": PLUGIN_DIR, "cache": CACHE_PARH, "setting": SETTING_PATH, "work_dir": WORK_DIR, "log": LOG_PATH},
								"plugin": {"reply": reply_plugin, "timeline": timeline_plugin, "event": event_plugin, "thread": thread_plugin, "regular": regular_plugin}
					}
					plugin.do(gvars)
				else:
					result = plugin.do()
			wait_time = 60 - datetime.datetime.now().second
			datetime_hour = datetime.datetime.now().hour
			datetime_minute = datetime.datetime.now().minute
			time.sleep(wait_time)
			for plugin in regular_plugin:
				if 'RATIO' in dir(plugin):
					ratio = plugin.RATIO
				else:
					ratio = 1
				if random.randint(1, ratio) != 1: #1/RATIOの確率でプラグイン実行
					continue
				if 'HOUR' in dir(plugin):
					hour = plugin.HOUR
				else:
					hour = None
				if 'MINUTE' in dir(plugin):
					minute = plugin.MINUTE
				else:
					minute = None
				if hour != None and minute != None:
					if hour == datetime_hour and minute == datetime_minute: #時と分指定型
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif hour != None:
					if hour == datetime_hour: #時だけ指定型(その時だけ毎分実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif minute != None:
					if minute == datetime_minute: #分だけ指定型(その分だけ毎時実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				#ある倍数の時だけ実行する
				if 'MULTIPLE_HOUR' in dir(plugin):
					multiple_hour = plugin.MULTIPLE_HOUR
				else:
					multiple_hour = None
				if 'MULTIPLE_MINUTE' in dir(plugin):
					multiple_minute = plugin.MULTIPLE_MINUTE
				else:
					multiple_minute = None
				if hour != None and minute != None:
					if datetime_hour % hour == 0 and datetime_minute % minute == 0: #時と分の倍数指定型
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif hour != None:
					if datetime_hour % hour == 0: #時だけ倍数指定型(その倍数時だけ毎分実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue
				elif minute != None:
					if datetime_minute % minute == 0: #分だけ倍数指定型(その倍数分だけ毎時実行)
						try:
							do(plugin)
						except Exception as e:
							logger.warning('プラグイン "%s" でエラーが発生しました\n詳細: %s' % (plugin.NAME, e))
						continue

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
			logger.info('プラグイン「%s」は有効になりました。' % name)
		except Exception as e:
			logger.warning('プラグイン「%s」は壊れています。有効にできませんでした。\nエラーログ: %s' % (name, e))

	def on_modified(self, event):
		if event.is_directory:
			return
		if not event.src_path.endswith('.py'):
			return
		InitializePlugins(init=False)

	def on_deleted(self, event):
		if event.is_directory:
			return
		if not event.src_path.endswith('.py'):
			return
		InitializePlugins(init=False)

if __name__ == '__main__':
	"""設定データを読み込み"""
	global  SETTING_PATH
	SETTING_PATH = os.path.dirname(os.path.abspath(__file__)) + '/setting.yaml'
	setting = yaml.load(open(SETTING_PATH).read())

	""""パスを読み込み"""
	global  PLUGIN_DIR, WORK_DIR, CACHE_PARH, LOG_PATH
	PLUGIN_DIR = setting['PLUGIN_DIR']
	WORK_DIR = setting['WORK_DIR']
	CACHE_PARH = WORK_DIR + '/cache.json'
	LOG_PATH = setting['LOG_DIR']+'/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'

	"""ロガーを準備"""
	global logger
	handler = logging.FileHandler(LOG_PATH, 'w', encoding='UTF-8')
	formatter = logging.Formatter('[%(levelname)s]%(asctime)s - %(message)s')
	handler.setFormatter(formatter)
	logger = logging.getLogger()
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)

	"""プラグインを格納するリストを定義"""
	global reply_plugin, timeline_plugin, event_plugin, thread_plugin, regular_plugin
	reply_plugin = []
	timeline_plugin = []
	event_plugin = []
	thread_plugin = []
	regular_plugin = []

	"""UserStreamに接続するアカウントの認証"""
	auth = tweepy.OAuthHandler(setting['CONSUMER_KEY'], setting['CONSUMER_SECRET'])
	auth.set_access_token(setting['ACCESS_TOKEN'], setting['ACCESS_TOKEN_SECRET'])
	global API
	API = tweepy.API(auth)
	SN = setting['SCREEN_NAME']

	"""プラグイン初期化"""
	InitializePlugins()

	""""キャッシュ or データベース"""
	global CACHE
	CACHE = {}
	#保管済のキャッシュがあれば読み込み
	try:
		CACHE = eval(open(CACHE_PARH, 'r').read())
		logger.info('前回のキャッシュを読み込みました。')
	except:
		pass

	"""別スレッドで処理するスレッドを起動"""
	[x.do().start() for x in thread_plugin]
	ScheduleTask().start()
	threading.Thread(name='SaveCache', target=SaveCache, args=()).start()

	""""プラグインディレクトリを監視"""
	event_handler = ChangeHandler()
	observer = Observer()
	observer.schedule(event_handler, PLUGIN_DIR, recursive=False)
	observer.start()

	logger.info('起動完了')

	"""UserStreamに接続"""
	while True:
		try:
			UserStream(auth, StreamListener()).user_stream()
		except:
			logger.warning('UserStreamから切断されました。10秒後に再接続します。')
			time.sleep(10)
