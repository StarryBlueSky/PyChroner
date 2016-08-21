# coding=utf-8
import logging
import urllib.parse

import tweepy

from TBFW.configparser import ConfigParser

logger = logging.getLogger(__name__)

def TwitterAPI(accountId):
	Config = ConfigParser()
	accounts = Config.accounts

	auth = tweepy.OAuthHandler(accounts[accountId]["ck"], accounts[accountId]["cs"])
	auth.set_access_token(accounts[accountId]["at"], accounts[accountId]["ats"])
	return tweepy.API(auth)

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
