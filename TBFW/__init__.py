# coding=utf-8

"""
TBFW library
"""

__version__ = "2.0.0"
__author__ = "Nephy Project Team"
__license__ = "MIT"

from TBFW.core import Core as Bot
from TBFW.twitterapi import TwitterAPI
import TBFW.exceptions as TBFWError

__all__ = ["Bot", "TwitterAPI", "TBFWError"]

if __name__ == "__main__":
	pass
