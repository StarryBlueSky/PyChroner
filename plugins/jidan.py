#! python3
# -*- coding: utf-8 -*-

TARGET = 'REPLY'

def do(stream):
	if 'jidan' in stream['text']:
		text = '@%s 試合を終えて家路へ向かうサッカー部員達。 疲れからか、不幸にも黒塗りの高級車に追突してしまう。後輩をかばいすべての責任を負った三浦(@%s)に対し、 車の主、暴力団員谷岡に言い渡された示談の条件とは・・・。' % (stream['user']['screen_name'], stream['user']['screen_name'])
		result = {"text": text, "in_reply_to": stream['id']}
		return result