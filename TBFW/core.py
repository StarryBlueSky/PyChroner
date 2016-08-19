# coding=utf-8
import TBFW.constant

class Core:
	"""
	The core of TBFW
	"""
	def __init__(self, root):
		self.path = {
			"current": root.rstrip("/") if root.endswith("/") else root,
			"plugins": TBFW.constant.pluginsDir,
			"assets": TBFW.constant.assetsDir,
			"tmp": TBFW.constant.tmpDir
		}

	def Start(self):
		""""パスを読み込み"""
		global PLUGIN_DIR, DATA_DIR
		PLUGIN_DIR = Set['path']['base'] + Set['path']['plugin']
		DATA_DIR = Set['path']['base'] + Set['path']['data']
		# ディレクトリがない場合は生成
		if not os.path.isdir(PLUGIN_DIR):
			os.makedirs(PLUGIN_DIR)
		if not os.path.isdir(DATA_DIR):
			os.makedirs(DATA_DIR)

		"""ロガーを準備"""
		handler = FileHandler(Set['path']['base'] + Set['path']['log'] + '/logger/' + datetime.datetime.now().strftime(
			'%Y-%m-%d_%H-%M-%S') + '.log', 'w', encoding='utf-8')
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
