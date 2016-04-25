#! python3
# -*- coding: utf-8 -*-
import datetime, urllib

TARGET = 'TIMELINE'

def do(stream):
	if stream['user']['screen_name'] == 'eewbot':
		minute = datetime.datetime.now().minute
		data = stream['text'].split(',')
		if eval(data[0]) != 39 and data[12] != '1' and data[12] != '不明':
			if eval(data[13]) == 0:
				tsunami = '震源は海底ではありません'
			else:
				tsunami = '震源は海底です。津波の情報など最新の情報に注意してください。'
			cache = '/my/tmp/eewbot.png'
			if '沖' in data[9]:
				z = '7'
			else:
				z = '8'
			urllib.request.urlretrieve('http://map.olp.yahooapis.jp/OpenLocalPlatform/V1/static?appid=dj0zaiZpPWxTYXBUTXBub0NRWSZzPWNvbnN1bWVyc2VjcmV0Jng9Yzg-&pin=' + data[7] + ',' + data[8] + '&z=' + z + '&mode=hybrid', cache)
			text = '【緊急地震速報】\n発生時刻: ' + data[6] + '\n震源: N' + data[7] + ' E' + data[8] + ' 深さ ' + data[10] + 'km\n※' + tsunami + '\n震央: ' + data[9] + '\n' + '最大震度: ' + data[12] + ' M' + data[11]
			result = {"text": text, "filename": cache}
			return result
