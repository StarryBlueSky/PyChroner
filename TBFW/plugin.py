# coding=utf-8
import logging
import os
import re
from importlib import machinery

from TBFW.constant import pluginAttributeTarget
from TBFW.constant import pluginAttributePriority
from TBFW.constant import pluginAttributeAttachedStream
from TBFW.constant import pluginAttributeRatio
from TBFW.constant import pluginAttributeHour
from TBFW.constant import pluginAttributeMultipleHour
from TBFW.constant import pluginAttributeMinute
from TBFW.constant import pluginAttributeMultipleMinute
from TBFW.constant import defaultAttributePriority
from TBFW.constant import defaultAttributeAttachedStream
from TBFW.constant import defaultAttributeRatio
from TBFW.constant import pluginTypes
from TBFW.constant import pluginReply, pluginTimeline, pluginEvent
from TBFW.constant import pluginThread, pluginRegular, pluginOther
from TBFW.exceptions import InvalidPluginSyntaxError
from TBFW.exceptions import InValidPluginFilenameError
from TBFW.exceptions import InvalidPluginTargetError
from TBFW.exceptions import NotFoundPluginTargetError

pluginFilePattern = re.compile("[^.].*\.py$")
logger = logging.getLogger(__name__)

class Plugin:
	def __init__(self, pluginPath):
		self.plugin = None
		self.attributePath = pluginPath
		self.attributeName = self.attributePath.split("/")[-1][:-3]
		self.attributeTarget = None
		self.attributePriority = None
		self.attributeAttachedStream = None
		self.attributeRatio = None
		self.attributeHour = None
		self.attributeMultipleHour = None
		self.attributeMinute = None
		self.attributeMultipleMinute = None

	def isValid(self):
		if pluginFilePattern.match(self.attributePath):
			return True
		else:
			return False

	def load(self):
		if self.isValid():
			try:
				loader = machinery.SourceFileLoader(self.attributeName, self.attributePath)
				plugin = loader.load_module(self.attributeName)
			except Exception as error:
				logger.warning(
					"Plugin \"{0}\"({1}) could not be loaded. Error Detail:\n{2}"
						.format(self.attributeName, self.attributePath, error)
				)
				raise InvalidPluginSyntaxError

			self.plugin = plugin

			if not hasattr(plugin, pluginAttributeTarget):
				raise NotFoundPluginTargetError
			if getattr(plugin, pluginAttributeTarget) not in pluginTypes:
				raise InvalidPluginTargetError
			self.attributeTarget = getattr(plugin, pluginAttributeTarget)
			delattr(plugin, pluginAttributeTarget)

			self.attributePriority = getattr(plugin, pluginAttributePriority) \
				if hasattr(plugin, pluginAttributePriority) else defaultAttributePriority
			delattr(plugin, pluginAttributePriority)

			self.attributeAttachedStream = getattr(plugin, pluginAttributeAttachedStream) \
				if hasattr(plugin, pluginAttributeAttachedStream) else defaultAttributeAttachedStream
			delattr(plugin, pluginAttributeAttachedStream)

			self.attributeRatio = getattr(plugin, pluginAttributeRatio) \
				if hasattr(plugin, pluginAttributeRatio) else defaultAttributeRatio
			delattr(plugin, pluginAttributeRatio)

			logger.info(
				"Plugin \"{0}\"({1}) has been loaded successfully."
					.format(self.attributeName, self.attributePath)
			)

		raise InValidPluginFilenameError


class PluginManager:
	def __init__(self, pluginsDir):
		self.pluginsDir = pluginsDir
		self.plugins = {}
		self.initializePlugins()

		self.usedStream = []

	def initializePlugins(self):
		self.plugins = {plugin_type: [] for plugin_type in pluginTypes}

	def appendPlugin(self, pluginPath):
		plugin = Plugin(pluginPath)
		if plugin.attributeAttachedStream not in self.usedStream:
			self.usedStream.append(plugin.attributeAttachedStream)

	def searchAllPlugins(self):
		self.initializePlugins()

		for pluginFile in os.listdir(self.pluginsDir):
			pluginPath = self.pluginsDir + "/" + pluginFile
			self.appendPlugin(pluginPath)

		# 定期実行プラグインで実行時間のパースをする
		tmp = []
		for plugin in self.plugins[pluginRegular]:
			hours = []
			minutes = []
			if hasattr(plugin, pluginAttributeHour):
				if isinstance(plugin.HOUR, list):
					hours.extend(plugin.HOUR)
				else:
					hours.append(plugin.HOUR)
			if hasattr(plugin, pluginAttributeMinute):
				if isinstance(plugin.MINUTE, list):
					minutes.extend(plugin.MINUTE)
				else:
					minutes.append(plugin.MINUTE)
			if hasattr(plugin, pluginAttributeMultipleHour):
				if isinstance(plugin.MULTIPLE_HOUR, int):
					hours.extend([i * plugin.MULTIPLE_HOUR for i in range(24) if 0 <= i * plugin.MULTIPLE_HOUR < 24])
			if hasattr(plugin, pluginAttributeMultipleMinute):
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

		plugins[pluginRegular] = tmp
		# プラグインを優先順位に並べる
		plugins[pluginReply] = [x for x in sorted(plugins[pluginReply], key=lambda x: x.PRIORITY, reverse=True)]
		plugins[pluginTimeline] = [x for x in sorted(plugins[pluginTimeline], key=lambda x: x.PRIORITY, reverse=True)]
		plugins[pluginEvent] = [x for x in sorted(plugins[pluginEvent], key=lambda x: x.PRIORITY, reverse=True)]
		plugins[pluginThread] = [x for x in sorted(plugins[pluginThread], key=lambda x: x.PRIORITY, reverse=True)]
		plugins[pluginRegular] = [x for x in sorted(plugins[pluginRegular], key=lambda x: x.PRIORITY, reverse=True)]
		plugins[pluginOther] = [x for x in sorted(plugins[pluginOther], key=lambda x: x.PRIORITY, reverse=True)]
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