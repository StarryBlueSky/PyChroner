# -*- coding: utf-8 -*-

TARGET = 'REPLY'

def do(stream):
	#334が含まれるリプライのときの条件分岐
	if '334' in stream['text']:
		#返信されるツイート
		text = u'@%s なんでや、阪神関係ないやろ！' % stream['user']['screen_name']
		result = {"text": text, "in_reply_to": stream['id']}
		return result