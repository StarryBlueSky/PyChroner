# coding=utf-8
import TBFW.constant
import re
import os
import logging
from importlib import machinery

pluginFilePattern = re.compile("[^.].*\.py$")
logger = logging.getLogger(__name__)

class Plugin:
	def __init__(self, pluginPath):
		self.pluginPath = pluginPath

	def isValid(self):
		if pluginFilePattern.match(self.pluginPath):
			return True
		else:
			return False

	def load(self):
		if self.isValid():
			pluginName = self.pluginPath.split("/")[-1][:-3]
			try:
				loader = machinery.SourceFileLoader(pluginName, self.pluginPath)
				plugin = loader.load_module(pluginName)
				# 属性値の定義
				plugin.__METADATA__NAME__ = pluginName
				if not hasattr(plugin, "PRIORITY"):
					plugin.PRIORITY = 0
				if not hasattr(plugin, "STREAM"):
					plugin.STREAM = 1
				if not hasattr(plugin, "RATIO"):
					plugin.RATIO = 1
				usedStream.append(plugin.STREAM)
				plugins[plugin.TARGET.lower()].append(plugin)
				logger.info("プラグイン \"%s\"(%s/%s)は有効になりました。" % (name, PLUGIN_DIR, plugin_file))
			except Exception as e:
				logger.warning('プラグイン \"%s\"(%s/%s)は有効にできませんでした。\nエラー詳細: %s' % (name, PLUGIN_DIR, plugin_file, e))
		return False

	def do(self):
		pass

class PluginManager:
	def __init__(self, pluginsDir):
		self.pluginsDir = pluginsDir
		self.plugins = {}

		self.initializePlugins()

	def initializePlugins(self):
		self.plugins = {plugin_type: [] for plugin_type in TBFW.constant.pluginTypes}

	def searchAllPlugins(self):

	def LoadPlugin(self):
		plugins = {
			"reply": [], "timeline": [], "event": [], "thread": [], "regular": [], "other": []}
		# PLUGIN_DIRから拡張機能読み込み

		for plugin_file in os.listdir(PLUGIN_DIR):
			self.pluginsDir + "/" +

		# 定期実行プラグインで実行時間のパースをする
		tmp = []
		for plugin in plugins["regular"]:
			hours = []
			minutes = []
			if hasattr(plugin, "HOUR"):
				if isinstance(plugin.HOUR, list):
					hours.extend(plugin.HOUR)
				else:
					hours.append(plugin.HOUR)
			if hasattr(plugin, "MINUTE"):
				if isinstance(plugin.MINUTE, list):
					minutes.extend(plugin.MINUTE)
				else:
					minutes.append(plugin.MINUTE)
			if hasattr(plugin, "MULTIPLE_HOUR"):
				if isinstance(plugin.MULTIPLE_HOUR, int):
					hours.extend([i * plugin.MULTIPLE_HOUR for i in range(24) if 0 <= i * plugin.MULTIPLE_HOUR < 24])
			if hasattr(plugin, "MULTIPLE_MINUTE"):
				if isinstance(plugin.MULTIPLE_MINUTE, int):
					minutes.extend([i * plugin.MULTIPLE_MINUTE for i in range(60) if 0 <= i * plugin.MULTIPLE_MINUTE < 60])
			hours = sorted(list(set(hours)))
			minutes = sorted(list(set(minutes)))
			if hours == []:
				hours = list(range(24))
			if minutes == []:
				minutes = list(range(60))
			plugin._HOURS = hours
			plugin._MINUTES = minutes
			tmp.append(plugin)
		plugins["regular"] = tmp
		# プラグインを優先順位に並べる
		plugins["reply"] = [x for x in sorted(plugins["reply"], key=lambda x: x.PRIORITY, reverse=True)]
		plugins["timeline"] = [x for x in sorted(plugins["timeline"], key=lambda x: x.PRIORITY, reverse=True)]
		plugins["event"] = [x for x in sorted(plugins["event"], key=lambda x: x.PRIORITY, reverse=True)]
		plugins["thread"] = [x for x in sorted(plugins["thread"], key=lambda x: x.PRIORITY, reverse=True)]
		plugins["regular"] = [x for x in sorted(plugins["regular"], key=lambda x: x.PRIORITY, reverse=True)]
		plugins["other"] = [x for x in sorted(plugins["other"], key=lambda x: x.PRIORITY, reverse=True)]
		# 読み込まれたプラグインの統計情報のJSONを出力
		result = []
		for type, _plugins in plugins.items():
			for plugin in _plugins:
				path = Set["path"]["base"] + Set["path"]["plugin"] + "/" + plugin._NAME + ".py"
				tmp = {
					"path": path, "size": os.path.getsize(path), "type": type, "isValid": True, "streamId": plugin.STREAM,
					"ratio": plugin.RATIO, "streamScreenName": Set["twitterSecret"][plugin.STREAM]["screen_name"],
					"name": plugin._NAME,}
				if type == "regular":
					tmp["hours"] = plugin._HOURS
					tmp["minutes"] = plugin._MINUTES
				result.append(tmp)
		json.dump(result, open(Set["path"]["base"] + Set["path"]["json"] + "/plugins.json", "w"))
		return plugins