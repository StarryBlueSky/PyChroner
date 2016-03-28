# -*- coding: utf-8 -*-

TARGET = 'TIMELINE'

def do(stream):
	#ぴょんが含まれるツイートのときの条件分岐
	if 'ぴょん' in stream['text']:
		#返信されるツイート
		text = u""""@%s こころぴょんぴょん待ち？✧ヾ(❀╹◡╹)ﾉﾞ考えるふりして(*≧o≦)b❤もうちょっと♡近づいちゃえ！☆♡ヾ(*'∀`*)ﾉ♡簡単には教えない(／≧∇)／＼(∇≦＼)／♪♡こんなに好きなことは✧:.ﾟ٩(๑>◡<๑)۶:.｡♡内緒なの～！((ヾ(๑ゝ･)ﾉ♡""" % stream['user']['screen_name']
		result = {"text": text, "in_reply_to": stream['id']}
		return result