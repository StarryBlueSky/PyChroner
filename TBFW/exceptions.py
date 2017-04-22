# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class BaseError(Exception):
    message = None

    def __str__(self):
        return self.message

class InValidPluginFilenameError(BaseError):
    message = "TBFW does not support that plugin's extension. Please check plugin's extension."

class NotFoundPluginTargetError(BaseError):
    message = "TBFW could not load plugin because of lacking of `TARGET` variable."

class InvalidPluginTargetError(BaseError):
    message = "TBFW could not load plugin because of unsupported target."

class InvalidPluginRatioError(BaseError):
    message = "TBFW could not load plugin because of not int type of RATIO."

class InvalidPluginSyntaxError(BaseError):
    message = "TBFW could not load plugin because of invalid syntax."

class InvalidPluginScheduleError(BaseError):
    message = "TBFW could not load plugin because of unsupported `HOUR` and `MINUTE` and so on."

class TooManyArgmentsForPluginError(BaseError):
    message = "TBFW could not load plugin because too many argments were required."

class InvalidConfigSyntax(BaseError):
    message = "TBFW could not start because config.json was invalid."

class NoAvailableAccountInConfig(BaseError):
    message = "TBFW could not start because there was no account in config."
