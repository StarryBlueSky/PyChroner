#! python3
# -*- coding: utf-8 -*-
import xmltodict, urllib, json

TARGET = 'REPLY'

def do(stream):
	if 'seq' in stream['text']:
		try:
			n = ' '.join(stream['text'].split(' ')[2:]).replace('+', '%2B').replace(' ', '+')
			data = xmltodict.parse(urllib.request.urlopen('http://api.wolframalpha.com/v2/query?input=' + str(n) + '&appid=X2AXJQ-GH4TJGT9Q6').read())
			data = json.loads(json.dumps(data))['queryresult']['pod']
			for x in data:
				if x['@title'] == 'Recurrence equation solution':
					path = '/my/tmp/seq.png'
					urllib.request.urlretrieve(x['subpod']['img']['@src'], path)
					text='@%s %s\n(%ss)' % (stream['user']['screen_name'], x['subpod']['plaintext'])
					result = {"text": text, "in_reply_to": stream['id'], "filename": path}
					break
				else:
					raise Exception
		except:
			text='@%s この数列は求められません。' % stream['user']['screen_name']
			result = {"text": text, "in_reply_to": stream['id']}

		return result