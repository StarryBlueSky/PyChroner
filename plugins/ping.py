#! python3
# -*- coding: utf-8 -*-
import time

TARGET = 'REPLY'

def getTime(status_id):
	created = ((status_id>>22)+1288834974657)/1000.0
	now = time.time()
	return str(now - created)

def do(stream):
	if 'ping' in stream['text']:
		text = '@%s Pong! Returned in %ss' % (stream['user']['screen_name'], getTime(stream['id']))
		result = {"text": text, "in_reply_to": stream['id']}
		return result