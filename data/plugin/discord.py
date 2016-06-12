#python3
# -*- coding: utf-8 -*-
import tweepy

TARGET = 'REGULAR'
MULTIPLE_HOUR = 6

def do(args):
	Set = args['set']
	auth = tweepy.OAuthHandler(Set['twitterSecret'][2]['ck'], Set['twitterSecret'][2]['cs'])
	auth.set_access_token(Set['twitterSecret'][2]['at'], Set['twitterSecret'][2]['ats'])
	API = tweepy.API(auth)

	text='【お知らせ】参加した試合ごとに統計を通知する機能を有効にするには https://app.zoraru.info/settings で設定を変更してください。トップキル / 目標達成なども通知されます。'
	API.update_status(status=text)
