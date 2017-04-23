# coding=utf-8

configPath = "config.json"

messageSuccessExecutingRegularPlugin = "Regular plugin \"{0}\" was executed successfully."
messageErrorExecutingRegularPlugin = "Regular plugin \"{0}\" could not be executed. Error Detail:\n{1}"
messageSuccessConnectingUserStream = "TBFW started @{0}'s streaming."
messageErrorConnectingUserStream = "Error occured while connecting to @{0}'s stream. TBFW will reconnect after {1} seconds."
messageErrorProcessingStream = "Error occured while processing @{0}'s stream."
messageErrorExecutingPlugin = "Error occured while executing plugin \"{0}\"."
messageTweetErrorExecutingPlugin = "@{0} Error occured while executing plugin \"{1}\". Please retry in minutes.\n\n詳細: {2}"
messageErrorConnectingTwitter = "Error occured while connecting to Twitter with HTTP Status Code {0}."

reconnectUserStreamSeconds = 10

pluginAttributeTarget = "TARGET"
pluginAttributePriority = "PRIORITY"
pluginAttributeAttachedStream = "ACCOUNT"
pluginAttributeRatio = "RATIO"
pluginAttributeHour = "HOUR"
pluginAttributeMultipleHour = "MULTIPLE_HOUR"
pluginAttributeMinute = "MINUTE"
pluginAttributeMultipleMinute = "MULTIPLE_MINUTE"

dayStartHour = 0
oneHourMinutes = 60
oneDayHours = 24
