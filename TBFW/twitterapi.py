# coding=utf-8
import logging
import urllib.parse

import tweepy

logger = logging.getLogger(__name__)

class TwitterAPI:
	def __init__(self):
		pass

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
