# coding=utf-8
"""
Base exception class
"""

from logging import getLogger

logger = getLogger(__name__)

class BaseError(Exception):
    """
    Represent base exception class
    """

    def __init__(self, message):
        self.msg = message

    def __str__(self):
        logger.exception(self.msg)
        return self.msg
