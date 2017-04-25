# coding=utf-8
"""
Base exception class
"""

class BaseError(Exception):
    """
    Represent base exception class
    """

    def __init__(self, message):
        self.msg = message

    def __str__(self):
        return self.msg
