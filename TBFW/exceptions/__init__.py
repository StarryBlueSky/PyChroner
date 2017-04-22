# coding=utf-8
import logging

logger = logging.getLogger(__name__)

class BaseError(Exception):
    message = None

    def __str__(self):
        logger.exception(self.message)
        return self.message
