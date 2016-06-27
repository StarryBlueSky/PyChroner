# coding=utf-8
import tweepy

class Bot:
	def __init__(self):
		self.reply_plugin = []
		self.timeline_plugin = []
		self.event_plugin = []
		self.regular_plugin = []
		self.thread_plugin = []

	def LoadPlugin(self):
		plugins = {}