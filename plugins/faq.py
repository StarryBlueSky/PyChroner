#! python3
# -*- coding: utf-8 -*-

TARGET = 'REPLY'

def do(stream):
	if 'faq' in stream['text']:
		text = '@%s よくある質問はこちらを御覧ください。→https://doc.zoraru.info/faq' %stream['user']['screen_name']
		result = {"text": text, "in_reply_to": stream['id']}
		return result