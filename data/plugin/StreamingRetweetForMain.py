#python3
# -*- coding: utf-8 -*-
import os
import DBInfo
import CommonDB
from pymongo import MongoClient

TARGET = 'TIMELINE'
STREAM = 1

connect = MongoClient(DBInfo.Host)
db = connect.bot
db.authenticate(DBInfo.Username, DBInfo.Password, mechanism='MONGODB-CR')

def do(stream, args):
	if not stream['user']['screen_name'] in [x['screen_name'] for x in args['set']['twitterSecret']]\
		and db['lastFollowId'].count({"id": stream['user']['id']}) == 1 and db['lastFollowerId'].count({"id": stream['user']['id']}) == 1:
		db['tweet'].insert(stream)

		# 画像を保存
		if "media" in stream['entities']:
			if not os.access(CommonDB.Set()['path']['base'] + CommonDB.Set()['path']['data'] + '/cache/tweet_image/' + str(stream['user']['id']), os.F_OK):
				os.makedirs(CommonDB.Set()['path']['base'] + CommonDB.Set()['path']['data'] + '/cache/tweet_image/' + str(stream['user']['id']))
						i = 1
						for x in stream['entities']['media']:
							ext = os.path.splitext(x['media_url_https'])[1]
							urllib.request.urlretrieve(x['media_url_https'], CommonDB.Set()['path']['base'] + CommonDB.Set()['path']['data'] + '/cache/tweet_image/' + str(stream['user']['id']) + '/' + str(stream['id']) + '_' + str(i) + ext)
							i += 1
				if stream['user']['screen_name'] == ME_MAIN and stream['text'].startswith("RT"):
					db7.execute("INSERT INTO ids VALUES ('%s')" % str(stream['retweeted_status']['id']))
				elif stream['text'].startswith("RT"):
					if db7.execute("SELECT * FROM ids WHERE tweet_id = '%s'" % stream['retweeted_status']['id']).fetchone():
						SendMessage('@%sがあなたがRTしたツイート「%s」(%s)をRTしました。' % (stream['user']['screen_name'], re.sub('^.*?(: )', '', stream['text']), 'https://twitter.com/' + stream['user']['screen_name'] + '/status/' + str(stream['id'])), channel='#twitter')
				DB_USER[str(stream['user']['id'])] = stream['user']