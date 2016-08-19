# coding=utf-8
import logging
import os
import re
from importlib import machinery

from TBFW.constant import defaultAttributeAttachedStream
from TBFW.constant import defaultAttributePriority
from TBFW.constant import defaultAttributeRatio
from TBFW.constant import pluginAttributeAttachedStream
from TBFW.constant import pluginAttributeHour
from TBFW.constant import pluginAttributeMinute
from TBFW.constant import pluginAttributeMultipleHour
from TBFW.constant import pluginAttributeMultipleMinute
from TBFW.constant import pluginAttributePriority
from TBFW.constant import pluginAttributeRatio
from TBFW.constant import pluginAttributeTarget
from TBFW.constant import pluginRegular
from TBFW.constant import pluginTypes
from TBFW.constant import oneDayHours, oneHourMinutes
from TBFW.exceptions import InValidPluginFilenameError
from TBFW.exceptions import InvalidPluginSyntaxError
from TBFW.exceptions import InvalidPluginTargetError
from TBFW.exceptions import NotFoundPluginTargetError

pluginFilePattern = re.compile("[^.].*\.py$")
logger = logging.getLogger(__name__)

class Plugin:
	def __init__(self, pluginPath):
		self.plugin = None
		self.attributeValid = None
		self.attributePath = pluginPath
		self.attributeSize = None
		self.attributeName = self.attributePath.split("/")[-1][:-3]
		self.attributeTarget = None
		self.attributePriority = None
		self.attributeAttachedStream = None
		self.attributeRatio = None
		self.attributeHour = None
		self.attributeMinute = None
		self.attributeMultipleHour = None
		self.attributeMultipleMinute = None

	def isValid(self):
		if pluginFilePattern.match(self.attributePath):
			self.attributeValid = True
			return True
		else:
			self.attributeValid = False
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

			if pluginAttributeTarget == pluginRegular:
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
						hours.extend([i * plugin.MULTIPLE_HOUR for i in range(oneDayHours) if 0 <= i * plugin.MULTIPLE_HOUR < oneDayHours])
				if hasattr(plugin, pluginAttributeMultipleMinute):
					if isinstance(plugin.MULTIPLE_MINUTE, int):
						minutes.extend([i * plugin.MULTIPLE_MINUTE for i in range(oneHourMinutes) if 0 <= i * plugin.MULTIPLE_MINUTE < oneHourMinutes])
				hours = sorted(list(set(hours)))
				minutes = sorted(list(set(minutes)))
				if hours == []:
					hours = list(range(oneDayHours))
				if minutes == []:
					minutes = list(range(oneHourMinutes))
				plugin._HOURS = hours
				plugin._MINUTES = minutes

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
		self.plugins = {pluginType: [] for pluginType in pluginTypes}

	def appendPlugin(self, pluginPath):
		plugin = Plugin(pluginPath)
		if plugin.attributeAttachedStream not in self.usedStream:
			self.usedStream.append(plugin.attributeAttachedStream)

	def searchAllPlugins(self):
		self.initializePlugins()

		for pluginFile in os.listdir(self.pluginsDir):
			pluginPath = self.pluginsDir + "/" + pluginFile
			self.appendPlugin(pluginPath)

		# プラグインを優先順位に並べる
		for pluginType in pluginTypes:
			self.plugins[pluginType] = [x for x in sorted(self.plugins[pluginType], key=lambda x: getattr(x, pluginAttributePriority), reverse=True)]

	def dumpPluginsList(self):
		result = []
		for pluginType, currentPlugins in self.plugins.items():
			for plugin in currentPlugins:
				tmp = {
					"path": plugin.attributePath,
					"size": os.path.getsize(plugin.attributePath),
					"type": pluginType.lower(),
					"isValid": plugin.attributeValid,
					"attachedStream": plugin.attributeAttachedStream,
					"ratio": plugin.attributeRatio,
					"name": plugin.attributeName
				}
				if pluginType == pluginRegular:
					tmp["hours"] = plugin.attributeHour
					tmp["minutes"] = plugin.attributeMinute
				result.append(tmp)
		return result
