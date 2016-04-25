#! python3
# -*- coding: utf-8 -*-
import json, urllib.request

TARGET = 'REPLY'

def do(stream):
	if 'train' in stream['text']:
		data = json.loads(urllib.request.urlopen('https://rti-giken.jp/fhc/api/train_tetsudo/delay.json').read())
		result = []
		for x in data:
			result.append(x['name']+'('+x['company']+')')
		text = '@%s 遅延情報一覧です。\n%s'% (stream['user']['screen_name'], "\n".join(result))
		result = {"text": text, "in_reply_to": stream['id']}
		return result