# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class TBFWError(Exception):
    message = None

    def __init__(self):
        logger.exception(self.message)
        Exception.__init__(self, self.message)

    def __str__(self):
        return self.message

class InValidPluginFilenameError(TBFWError):
    message = "TBFW does not support that plugin's extension. Please check plugin's extension."

class NotFoundPluginTargetError(TBFWError):
    message = "TBFW could not load plugin because of lacking of `TARGET` variable."

class InvalidPluginTargetError(TBFWError):
    message = "TBFW could not load plugin because of unsupported target."

class InvalidPluginRatioError(TBFWError):
    message = "TBFW could not load plugin because of not int type of RATIO."

class InvalidPluginSyntaxError(TBFWError):
    message = "TBFW could not load plugin because of invalid syntax."

class InvalidPluginScheduleError(TBFWError):
    message = "TBFW could not load plugin because of unsupported `HOUR` and `MINUTE` and so on."

class TooManyArgmentsForPluginError(TBFWError):
    message = "TBFW could not load plugin because too many argments were required."

class InvalidConfigSyntax(TBFWError):
    message = "TBFW could not start because config.json was invalid."

class NoAvailableAccountInConfig(TBFWError):
    message = "TBFW could not start because there was no account in config."
