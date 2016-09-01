# coding=utf-8
import time

from ..TBFW import TwitterAPI

TARGET = "REPLY"
ACCOUNT = 0

def getPing(tweetid):
	created = ((tweetid>>22)+1288834974657)/1000.0
	now = time.time()
	return float(now - created)

def do(stream):
	if "ping" in stream["text"]:
		replyTo = stream["user"]["screen_name"]
		ping = getPing(stream["id"])

		API = TwitterAPI(accountId=ACCOUNT)
		API.update_status("@{0} Pong in {1}s.".format(replyTo, ping))

