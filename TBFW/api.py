# coding=utf-8

class Plugin:
	"""
	Plugin base
	"""
	def __init__(self):
		pass

	def OnStream(self):
		"""calls when TBFW receives UserStream Data"""
		pass

	def OnTweet(self):
		"""calls when TBFW receives tweets"""
		pass

	def OnReply(self):
		"""calls when TBFW receives reply tweets (exclude retweets)"""
		pass

	def OnRetweet(self):
		"""calls when TBFW receives retweets"""
		pass

	def OnTimeline(self):
		"""calls when TBFW receives non-reply tweets (exclude retweets)"""
		pass

	def OnEvent(self):
		"""calls when TBFW receives UserStream event data"""
		pass

	def OnDelete(self):
		"""calls when TBFW receives delete data"""
		pass

	def OnOther(self):
		"""calls when TBFW receives other data"""
		pass
