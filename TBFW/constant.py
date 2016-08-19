# coding=utf-8

pathPluginsDir = "plugins"
pathAssetsDir = "assets"
pathCacheDir = "cache"
pathLogDir = "logs"
pathTmpDir = "tmp"

pluginReply = "reply"
pluginTimeline = "timeline"
pluginEvent = "event"
pluginThread = "thread"
pluginRegular = "regular"
pluginOther = "other"

pluginTypes = [
	pluginReply,
	pluginTimeline,
	pluginEvent,
	pluginThread,
	pluginRegular,
	pluginOther
]

messageLogFormat = "[%(levelname)s]%(asctime)s - %(message)s"
messageLogDatetimeFormat = "%Y-%m-%d_%H-%M-%S"
messageSuccessInitialization = "Initialization Complate. Current time is {0}."
messageErrorLoadingPlugin = "Plugin \"{0}\"({1}) could not be loaded. Error Detail:\n{2}"
messageSuccessLoadingPlugin = "Plugin \"{0}\"({1}) has been loaded successfully."

acceptLanguage = "ja;q=1.0"
userAgent = "TwitterBotFramework/3.0 (Python 3)"

pluginAttributeTarget = "TARGET"
pluginAttributePriority = "PRIORITY"
pluginAttributeAttachedStream = "STREAM"
pluginAttributeRatio = "RATIO"
pluginAttributeHour = "HOUR"
pluginAttributeMultipleHour = "MULTIPLE_HOUR"
pluginAttributeMinute = "MINUTE"
pluginAttributeMultipleMinute = "MULTIPLE_MINUTE"

defaultAttributeValid = None
defaultAttributePath = None
defaultAttributeSize = None
defaultAttributeName = None
defaultAttributeTarget = None
defaultAttributePriority = 0
defaultAttributeAttachedStream = 0
defaultAttributeRatio = 1
defaultAttributeHour = None
defaultAttributeMultipleHour = None
defaultAttributeMinute = None
defaultAttributeMultipleMinute = None

dayStartHour = 0
oneHourMinutes = 60
oneDayHours = 24
