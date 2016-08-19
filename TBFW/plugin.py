# coding=utf-8
import logging
import os
import re
from importlib import machinery

from TBFW.constant import *
from TBFW.exceptions import *

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
		self.attributeHours = []
		self.attributeMinutes = []

	def isValid(self):
		if pluginFilePattern.match(self.attributePath):
			return True
		else:
			return False

	def load(self):
		if self.isValid():
			self.attributeValid = True
			self.attributeSize = os.path.getsize(self.attributePath)

			try:
				loader = machinery.SourceFileLoader(self.attributeName, self.attributePath)
				plugin = loader.load_module(self.attributeName)
			except Exception as error:
				logger.warning(messageErrorLoadingPlugin.format(self.attributeName, self.attributePath, error))
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
				pluginHour = getattr(plugin, pluginAttributeHour) \
					if hasattr(plugin, pluginAttributeHour) else defaultAttributeHour
				pluginMinute = getattr(plugin, pluginAttributeMinute) \
					if hasattr(plugin, pluginAttributeMinute) else defaultAttributeMinute
				pluginMultipleHour = getattr(plugin, pluginAttributeMultipleHour) \
					if hasattr(plugin, pluginAttributeMultipleHour) else defaultAttributeMultipleHour
				pluginMultipleMinute = getattr(plugin, pluginAttributeMultipleMinute) \
					if hasattr(plugin, pluginAttributeMultipleMinute) else defaultAttributeMultipleMinute

				if pluginHour != defaultAttributeHour:
					if isinstance(pluginHour, list):
						hours.extend(plugin.HOUR)
					elif isinstance(pluginHour, int):
						hours.append(plugin.HOUR)
					else:
						raise InvalidPluginScheduleError

				if pluginMinute != defaultAttributeMinute:
					if isinstance(plugin.MINUTE, list):
						minutes.extend(plugin.MINUTE)
					elif isinstance(pluginMinute, int):
						minutes.append(plugin.MINUTE)
					else:
						raise InvalidPluginScheduleError

				if pluginMultipleHour != defaultAttributeMultipleHour:
					if isinstance(plugin.MULTIPLE_HOUR, int):
						hours.extend(
							[i * plugin.MULTIPLE_HOUR for i in range(oneDayHours) if dayStartHour <= i * plugin.MULTIPLE_HOUR < oneDayHours]
						)
					else:
						raise InvalidPluginScheduleError

				if pluginMultipleMinute != defaultAttributeMultipleMinute:
					if isinstance(plugin.MULTIPLE_MINUTE, int):
						minutes.extend(
							[i * plugin.MULTIPLE_MINUTE for i in range(oneHourMinutes) if dayStartHour <= i * plugin.MULTIPLE_MINUTE < oneHourMinutes]
						)
					else:
						raise InvalidPluginScheduleError

				hours = sorted(list(set(hours)))
				minutes = sorted(list(set(minutes)))
				if hours == list():
					hours = list(range(oneDayHours))
				if minutes == list():
					minutes = list(range(oneHourMinutes))
				self.attributeHours = hours
				self.attributeMinutes = minutes

			logger.info(messageSuccessLoadingPlugin.format(self.attributeName, self.attributePath))

		else:
			self.attributeValid = False
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
					"size": plugin.attributeSize,
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
