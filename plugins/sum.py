# -*- coding: utf-8 -*-
import xmltodict, urllib, json

TARGET = 'REPLY'

def do(stream):
	if 'sum' in stream['text']:
		k = stream['text'].split(' ')[2]
		n = 'Sum[%s, {k, 1, n}]' % k
		data = xmltodict.parse(urllib.request.urlopen('http://api.wolframalpha.com/v2/query?input=' + n.replace(' ', '+') + '&appid=X2AXJQ-GH4TJGT9Q6').read())
		data = json.loads(json.dumps(data))['queryresult']['pod'][0]
		path = '/my/tmp/sum.png'
		urllib.request.urlretrieve(data['subpod']['img']['@src'], path)
		text = '@%s 数列a_k=%sの和です。' % (stream['user']['screen_name'], k)
		result = {"text": text, "in_reply_to": stream['id'], "filename": path}
		return result