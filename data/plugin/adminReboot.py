#! python3
# -*- coding: utf-8 -*-
import Twitter
import re

TARGET = 'REPLY'

def do(stream):
	texted = re.sub('@.+?(\s|\t|$)', '', stream['text'])
	if 'あの' in texted:
		Twitter.Post(text='@%s はい' % stream['user']['screen_name'], stream=stream, tweetid=stream['id'])