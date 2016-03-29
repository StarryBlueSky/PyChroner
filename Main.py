# -*- coding: utf-8 -*-
import imp, re, urllib, json, threading, logging, random, os, datetime, time
import tweepy
import yaml

"""初期化する関数: プラグインを再読み込みする"""
def InitializePlugins():
	plugins = {}
	"""PLUGIN_DIRから拡張機能読み込み"""
	for plugin_file in os.listdir(PLUGIN_DIR):
		if re.compile('[^.].*\.py$').match(plugin_file):
			name = plugin_file[:-3]
			try:
				ext_info = imp.find_module(name, [PLUGIN_DIR])
				plugin = imp.load_module(name, *ext_info)
				plugin.NAME = name
				plugins[name] = plugin
				logging.info(u'プラグイン「%s」は有効になりました。' % name)
			except:
				logging.info(u'プラグイン「%s」は壊れています。有効にできませんでした。文法を確認してください。' % name)
	"""pluginの種類を分類"""
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
			thread_plugin.append(plugin)
	logging.info(u"""プラグインの一覧:
						リプライプラグイン: %s
						タイムラインプラグイン: %s
						イベントプラグイン: %s
						スレッドプラグイン: %s
						定期実行プラグイン: %s
						"""
				 % (str(reply_plugin), str(timeline_plugin), str(event_plugin), str(thread_plugin), str(regular_plugin)))

"""プラグインの結果をツイートする関数"""
def Post(text, stream, dm=False, lat=None, longs=None, in_reply_to_status_id=None, filename=None):
	try:
		if dm == True:
			API.send_direct_message(screen_name=stream['user']['screen_name'], text=text)
		elif filename == None:
			API.update_status(status=text, in_reply_to_status_id=in_reply_to_status_id, lat=lat, long=longs)
		else:
			API.update_with_media(filename=filename, status=text, in_reply_to_status_id=in_reply_to_status_id, lat=lat, long=longs)
		return True
	except tweepy.TweepError, e:
		code = e[0]
		if code == 186: # 186 = Status is over 140 characters
			Post(u'@%s ツイートが長すぎるため、DMで送信しました。' % stream['user']['screen_name'], stream, dm=False, lat=lat, longs=longs, in_reply_to_status_id=in_reply_to_status_id, filename=filename)
			Post(text, stream, dm=True, lat=lat, longs=longs, in_reply_to_status_id=in_reply_to_status_id, filename=filename)
			return True
		elif code in [150, 187, 226]:
			logging.warning(u'Twitter APIエラーが発生しました\n詳細: %s' % ' '.join(e))
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
			#名前欄攻撃対策
			stream['user']['name'] = stream['user']['name'].replace('@', u'@​')

			if re.match('@%s\s' % SN, stream['text'], re.IGNORECASE):
				for plugin in reply_plugin:
					ExecutePlugin(plugin, stream)

			for plugin in timeline_plugin:
				ExecutePlugin(plugin, stream)

		elif 'event' in stream:
			for plugin in event_plugin:
				ExecutePlugin(plugin, stream)

	except Exception as e:
		print(e)

"""プラグインを実行する関数"""
def ExecutePlugin(plugin, stream):
	try:
		if 'RATIO' in dir(plugin):
			ratio = plugin.RATIO
		else:
			ratio = 1
		if random.randint(1, ratio) == 1: #1/RATIOの確率でプラグイン実行
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
			else:
				logging.debug(u'プラグイン "%s" の返り値が不正です\nプラグインは辞書かFalseをrerurnしてください' % plugin.NAME)
		elif result == False:
			raise Exception
	except Exception as e:
		if plugin.TARGET == 'REPLY': #リプライプラグインの時のみユーザーにエラーを知らせる
			text = u'@%s プラグイン "%s"でエラーが発生しました。\n\n詳細: %s' % (stream['user']['screen_name'], plugin.NAME, e)
			Post(text, stream)
		logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)

"""tweepyのクラスを継承してUserStreamを受信するクラス"""
class StreamListener(tweepy.StreamListener):
	def on_data(self, raw):
		if raw.startswith('{'):
			t = threading.Thread(target=StreamLine, name='StreamLine', args=(raw, ))
			t.start()
			t.join(20) #スレッドのタイムアウト 20秒
			if t.isAlive():
				t.__stop()
				logging.warning(u'スレッドがタイムアウトしました: %s' % raw)
			return True
		else:
			logging.warning(u'解析不能なUserStreamデータを受信しました: %s' % raw)
			return False
	def on_error(self, status_code):
		print(status_code)

"""tweepyのクラスを継承してUserStreamの設定をするクラス"""
class UserStream(tweepy.Stream):
	def user_stream(self):
		self.parameters = {"delimited": "length", "replies": "all", "filter_level": "none", "include_followings_activity": "True", "stall_warnings": "True", "with": "followings"}
		self.headers['Content-type'] = "application/x-www-form-urlencoded"
		self.scheme = "https"
		self.host = 'userstream.twitter.com'
		self.url = '/1.1/user.json'
		self.body = urllib.urlencode(self.parameters)
		self.timeout = None
		self._start(False)

"""定期実行するプラグインを実行するクラス"""
class ScheduleTask(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
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
							plugin.do()
						except Exception as e:
							logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)
						continue
				elif hour != None:
					if hour == datetime_hour: #時だけ指定型(その時だけ毎分実行)
						try:
							plugin.do()
						except Exception as e:
							logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)
						continue
				elif minute != None:
					if minute == datetime_minute: #分だけ指定型(その分だけ毎時実行)
						try:
							plugin.do()
						except Exception as e:
							logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)
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
							plugin.do()
						except Exception as e:
							logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)
						continue
				elif hour != None:
					if datetime_hour % hour == 0: #時だけ倍数指定型(その倍数時だけ毎分実行)
						try:
							plugin.do()
						except Exception as e:
							logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)
						continue
				elif minute != None:
					if datetime_minute % minute == 0: #分だけ倍数指定型(その倍数分だけ毎時実行)
						try:
							plugin.do()
						except Exception as e:
							logging.warning(u'プラグイン "%s" でエラーが発生しました\n詳細: %s' % plugin.NAME, e)
						continue

if __name__ == '__main__':
	"""設定データを読み込み"""
	SETTING_PATH = os.path.dirname(os.path.abspath(__file__)) + '/setting.yaml'
	setting = yaml.load(open(SETTING_PATH).read())

	""""パスを読み込み"""
	PLUGIN_DIR = setting['PLUGIN_DIR']
	WORK_DIR = setting['WORK_DIR']
	LOG_PATH = setting['LOG_DIR']+'/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'

	"""ロガーを準備"""
	logging.basicConfig(level=logging.INFO, filename=LOG_PATH, format='[%(levelname)s]%(asctime)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

	"""プラグインを格納するリストを定義"""
	global reply_plugin #@リプライに反応するプラグイン
	reply_plugin = []
	global timeline_plugin #タイムラインに反応するプラグイン
	timeline_plugin = []
	global event_plugin #UserStreamイベントに反応するプラグイン
	event_plugin = []
	global thread_plugin #スレッドで起動するプラグイン
	thread_plugin = []
	global regular_plugin #定期実行するプラグイン
	regular_plugin = []

	"""UserStreamに接続するアカウントの認証"""
	auth = tweepy.OAuthHandler(setting['CONSUMER_KEY'], setting['CONSUMER_SECRET'])
	auth.set_access_token(setting['ACCESS_TOKEN'], setting['ACCESS_TOKEN_SECRET'])
	global API
	API = tweepy.API(auth)
	SN = setting['SCREEN_NAME']

	"""プラグイン初期化"""
	InitializePlugins()

	"""別スレッドで処理するスレッドを起動"""
	[x.do().start() for x in thread_plugin]
	ScheduleTask().start()

	"""UserStreamに接続"""
	while True:
		UserStream(auth, StreamListener()).user_stream()
