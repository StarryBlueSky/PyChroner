#python3
# -*- coding: utf-8 -*-
import DBInfo
from pymongo import MongoClient

TARGET = 'REGULAR'

def do():
	connect = MongoClient(DBInfo.Host)
	db = connect.bot
	db.authenticate(DBInfo.Username, DBInfo.Password, mechanism='MONGODB-CR')

	db['Set'].update_one({}, {"$inc": {"daily_tweet": db['Set'].find_one()['minly_tweet']}})
	db['Set'].update_one({}, {"$inc": {"daily_event": db['Set'].find_one()['minly_event']}})
	db['Set'].update_one({}, {"$set": {"minly_tweet": 0}})
	db['Set'].update_one({}, {"$set": {"minly_event": 0}})