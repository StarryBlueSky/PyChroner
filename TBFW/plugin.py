# coding=utf-8
import TBFW.constant
import TBFW.exceptions
import re
import os
import logging
from importlib import machinery

pluginFilePattern = re.compile("[^.].*\.py$")
logger = logging.getLogger(__name__)

class Plugin:
	def __init__(self, pluginPath):
		self.plugin = None
		self.pluginPath = pluginPath
		self.pluginName = self.pluginPath.split("/")[-1][:-3]
		self.pluginTarget = None
		self.pluginPriority = None
		self.pluginAttachedStream = None
		self.pluginRatio = None

	def isValid(self):
		if pluginFilePattern.match(self.pluginPath):
			return True
		else:
			return False

	def load(self):
		if self.isValid():
			try:
				loader = machinery.SourceFileLoader(self.pluginName, self.pluginPath)
				plugin = loader.load_module(self.pluginName)

				self.pluginPriority = plugin.PRIORITY if not hasattr(plugin, "PRIORITY") else 0
				self.pluginAttachedStream = plugin.STREAM if not hasattr(plugin, "STREAM") else 0
				self.pluginRatio = plugin.RATIO if not hasattr(plugin, "RATIO") else 1

				self.plugin = plugin

				logger.info("Plugin \"%s\"(%s) has been loaded successfully." % (self.pluginName, self.pluginPath))

			except Exception as error:
				logger.warning("Plugin \"%s\"(%s) could not be loaded. Error Detail:\n%s" % (self.pluginName, self.pluginPath, error))
				raise TBFW.exceptions.InvalidPluginSyntaxError

		raise TBFW.exceptions.InValidPluginFilenameError

class PluginManager:
	def __init__(self, pluginsDir):
		self.pluginsDir = pluginsDir
		self.plugins = {}

		self.usedStream = []

		self.initializePlugins()

	def initializePlugins(self):
		self.plugins = {plugin_type: [] for plugin_type in TBFW.constant.pluginTypes}

	def searchAllPlugins(self):

	def LoadPlugin(self):
		plugins = {
			"reply": [], "timeline": [], "event": [], "thread": [], "regular": [], "other": []}
		# PLUGIN_DIRから拡張機能読み込み

		for pluginFile in os.listdir(self.pluginsDir):
			pluginPath = self.pluginsDir + "/" + pluginFile
			plugin = Plugin(pluginPath)
			self.usedStream.append(plugin.STREAM)

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