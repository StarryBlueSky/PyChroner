# -*- coding: utf-8 -*-
import fractions

TARGET = 'REPLY'

def do(stream):
	if 'gcm' in stream['text']:
		m = stream['text'].split(' ')[2]
		n = stream['text'].split(' ')[3]
		result = fractions.gcd(int(m), int(n))
		text=u'@%s %sと%sの最大公約数(GCM)は%sです。' % (stream['user']['screen_name'], m, n, result)
		result = {"text": text, "in_reply_to": stream['id']}
		return result