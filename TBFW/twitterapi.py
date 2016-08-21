# coding=utf-8
import tweepy
import time
import threading
import logging
import urllib.parse
from TBFW.constant import *
logger = logging.getLogger(__name__)

class TwitterAPI:
	def __init__(self):
		pass

	def startUserStream(self, n):
		auth = tweepy.OAuthHandler(Set['twitterSecret'][n]['ck'], Set['twitterSecret'][n]['cs'])
		auth.set_access_token(Set['twitterSecret'][n]['at'], Set['twitterSecret'][n]['ats'])
		sn = Set['twitterSecret'][n]['screen_name']
		while True:
			try:
				logger.info('@%sのUserStreamに接続しました。' % sn)
				UserStream(auth, StreamListener(n, sn)).user_stream()
			except:
				logger.warning('@%sのUserStreamから切断されました。10秒後に再接続します。エラーログ: \n%s' % (sn, traceback.format_exc()))
				time.sleep(reconnectUserStreamSeconds)

class StreamListener(tweepy.StreamListener):
	def __init__(self, n, sn):
		self.n = n
		self.sn = sn

	def on_data(self, raw):
		t = threading.Thread(target=StreamLine, name='StreamLine', args=(raw, self.n, self.sn))
		t.start()

	def on_error(self, status_code):
		logger.warning('Twitter APIエラーが発生しました\n詳細: HTTPステータスコード=%s' % status_code)

class UserStream(tweepy.Stream):
	def user_stream(self):
		self.parameters = {
			"delimited": "length",
			"replies": "all",
			"filter_level": "none",
			"include_followings_activity": "True",
			"stall_warnings": "True",
			"with": "followings"
		}
		self.headers['Content-type'] = "application/x-www-form-urlencoded"
		self.scheme = "https"
		self.host = 'userstream.twitter.com'
		self.url = '/1.1/user.json'
		self.body = urllib.parse.urlencode(self.parameters)
		self.timeout = None
		self._start(False)