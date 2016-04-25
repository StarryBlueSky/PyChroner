#! python3
# -*- coding: utf-8 -*-

TARGET = 'REPLY'

def do(stream):
	if 'setting' in stream['text'] or 'register' in stream['text'] or '設定' in stream['text'] or 'config' in stream['text']:
		text='@%s 設定はこちらで変更できます。\nhttps://zoraru.info/account/settings' % stream['user']['screen_name']
		result = {"text": text, "in_reply_to": stream['id']}
		return result