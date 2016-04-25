#! python3
# -*- coding: utf-8 -*-
import xmltodict, urllib, json

TARGET = 'REPLY'

def do(stream):
	if 'guessseq' in stream['text']:
		try:
			n = '+'.join(stream['text'].split(' ')[2:])
			data = xmltodict.parse(urllib.request.urlopen('http://api.wolframalpha.com/v2/query?input=' + str(n) + '&appid=X2AXJQ-GH4TJGT9Q6').read())
			data = json.loads(json.dumps(data))['queryresult']['pod'][-1]
			if data['@title'] == 'Possible sequence identification':
				path = '/my/tmp/guessseq'
				urllib.request.urlretrieve(data['subpod'][0]['img']['@src'], path)
				text='@%s %s' % (stream['user']['screen_name'], data['subpod'][1]['plaintext'])
				result = {"text": text, "in_reply_to": stream['id'], "filename": path}
			else:
				raise Exception
		except:
			text='@%s この数列は推定できません。' % stream['user']['screen_name']
			result = {"text": text, "in_reply_to": stream['id']}

		return result

