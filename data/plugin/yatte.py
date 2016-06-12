#! python3
# -*- coding: utf-8 -*-
import Twitter
import re, random

TARGET = 'REPLY'

def do(stream):
	texted = re.sub('@.+?(\s|\t|$)', '', stream['text'])
	if 'はい' in texted:
		if random.randint(0, 3) == 0:
			Twitter.Post(text='@%s はいじゃないが' % stream['user']['screen_name'], stream=stream, tweetid=stream['id'])
		else:
			Twitter.Post(text='@%s あの' % stream['user']['screen_name'], stream=stream, tweetid=stream['id'])