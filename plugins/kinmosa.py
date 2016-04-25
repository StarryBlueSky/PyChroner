#! python3
# -*- coding: utf-8 -*-
import datetime, math, random

TARGET = 'REPLY'

def do(stream):
	if 'kinmoza' in stream['text'] or 'kinmosa' in stream['text']:
		hour = datetime.datetime.now().hour
		minute = datetime.datetime.now().minute
		if '2' in stream['text']:
			minus = datetime.datetime.now() - datetime.datetime.strptime('2015-4-6 00:00:00', '%Y-%m-%d %H:%M:%S')
			weeks = math.floor(float(minus.days + minus.seconds/86400)/7)
			wordlist1 = ['はるが', 'プレゼント・フォー・', 'あなたが', '雨にも', 'おねえちゃんと', 'きになる', 'マイ・ディア・', 'もうすぐ', 'とっておきの', '海べの', 'ほんのすこしの', 'なによりとびきり']
			wordlist2 =  ['きたっ', 'ユー', 'とってもまぶしくて', 'まけず', 'あそぼう', 'あの子', 'ヒーロー', '夏休み', '一日', 'やくそく', '長いよる', '好きだから']
			title = str(random.choice(wordlist1).encode('utf8')) + str(random.choice(wordlist2).encode('utf8'))
			number = int(datetime.datetime.now().weekday())
			if number in [0,1,2,3,4,5]:
				if number == 0: x=6
				elif number == 1: x=5
				elif number == 2: x=4
				elif number == 3: x=3
				elif number == 4: x=2
				elif number == 5: x=1
				on_air = datetime.datetime.strptime('%s 00:00:00' % datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=x)
				text = '@%s 次回のハロー！きんいろモザイクはAT-Xで%s月%s日24時00分から\n%s話「%s」の放送です。お楽しみに。' % (stream['user']['screen_name'], on_air.strftime("%m"), on_air.strftime("%d"), int(math.floor(weeks)), title.decode('utf8'))
			else:
				if number == 5 and hour < 20 and minute < 30:
					text = '@%s 次回のハロー！きんいろモザイクはAT-Xでは今夜24時00分から\n%s話「%s」の放送です。お楽しみに。' % (stream['user']['screen_name'], int(math.floor(weeks)), title.decode('utf8'))
				elif hour == 0:
					title2 = str(random.choice(wordlist1).encode('utf8')) + str(random.choice(wordlist2).encode('utf8'))
					next_on_air = datetime.datetime.strptime('%s 00:00:00' % datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=7)
					text = '@%s ハロー！きんいろモザイク %s話「%s」はAT-Xで現在放送中です。\n次回の放送は%s月%s日24時00分からの%s話「%s」です。お楽しみに。' % (stream['user']['screen_name'], int(math.floor(weeks)), title.decode('utf8'), next_on_air.strftime("%m"), next_on_air.strftime("%d"), int(math.floor(weeks))+1, title2.decode('utf8'))
				elif hour > 0:
					on_air = datetime.datetime.strptime('%s 00:00:00' % datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=7)
					text = '@%s 次回のハロー！きんいろモザイクはAT-Xで来週%s月%s日24時00分から\n%s話「%s」の放送です。お楽しみに。' % (stream['user']['screen_name'], on_air.strftime("%m"), on_air.strftime("%d"), int(math.floor(weeks)), title.decode('utf8'))
		else:
			minus = datetime.datetime.now() - datetime.datetime.strptime('2013-7-6 20:30:00', '%Y-%m-%d %H:%M:%S')
			weeks = math.floor(float(minus.days + minus.seconds/86400)/7)
			wordlist1 = ['ふしぎの国の', 'ちっちゃくたって', 'どんな', 'あめどきどき', 'おねえちゃんと', '金の', 'はらぺこ', 'すてきな', 'ねないこ', 'きょうは', 'どんなに', 'きんいろの', 'どきどき', 'はじめまして']
			wordlist2 =  ['アリス', 'カレン', 'トモダチできるかな', 'あやや', 'ようこ', 'しの', 'とき', '五にんぐみ', 'あててごらん', 'なんの日?', 'さくら', 'あげぽよ', 'からすちゃん']
			title = str(random.choice(wordlist1).encode('utf8')) + str(random.choice(wordlist2).encode('utf8'))
			number = int(datetime.datetime.now().weekday())
			if number in [0,1,2,3,4,6]:
				if number == 0: x=5
				elif number == 1: x=4
				elif number == 2: x=3
				elif number == 3: x=2
				elif number == 4: x=1
				elif number == 6: x=6
				on_air = datetime.datetime.strptime('%s 20:30:00' % datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=x)
				text = '@%s 次回のきんいろモザイクはAT-Xで%s月%s日20時30分から\n%s話「%s」の放送です。お楽しみに。' % (stream['user']['screen_name'], on_air.strftime("%m"), on_air.strftime("%d"), int(math.floor(weeks)), title.decode('utf8'))
			else:
				if number == 5 and hour < 20 and minute < 30:
					text = '@%s 次回のきんいろモザイクはAT-Xでは今夜20時30分から\n%s話「%s」の放送です。お楽しみに。' % (stream['user']['screen_name'], int(math.floor(weeks)), title.decode('utf8'))
				elif hour == 20:
					title2 = str(random.choice(wordlist1).encode('utf8')) + str(random.choice(wordlist2).encode('utf8'))
					next_on_air = datetime.datetime.strptime('%s 20:30:00' % datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=7)
					text = '@%s きんいろモザイク %s話「%s」はAT-Xで現在放送中です。\n次回の放送は%s月%s日20時30分からの%s話「%s」です。お楽しみに。' % (stream['user']['screen_name'], int(math.floor(weeks)), title.decode('utf8'), next_on_air.strftime("%m"), next_on_air.strftime("%d"), int(math.floor(weeks))+1, title2.decode('utf8'))
				elif hour > 20:
					on_air = datetime.datetime.strptime('%s 20:30:00' % datetime.datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=7)
					text = '@%s 次回のきんいろモザイクはAT-Xで来週%s月%s日20時30分から\n%s話「%s」の放送です。お楽しみに。' % (stream['user']['screen_name'], on_air.strftime("%m"), on_air.strftime("%d"), int(math.floor(weeks)), title.decode('utf8'))

		result = {"text": text, "in_reply_to": stream['id']}
		return result