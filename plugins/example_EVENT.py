# -*- coding: utf-8 -*-
import yaml, os

TARGET = 'EVENT'

def do(stream):
	#ふぁぼのイベントのときの条件分岐
	if stream['event'] == 'favorite':
		#ターゲットが@AbeShinzoのときの条件分岐
		if stream['target'] == 'AbeShinzo':
			#設定読み込み
			setting = yaml.load(open(os.path.dirname(os.path.abspath(__file__)) + '/setting.yaml').read())
			#書き込みパス
			path = setting['WORK_DIR']+'/AbeFavs/' + str(stream['source']['id'])
			#ふぁぼ数を読み込み
			try:
				n = int(open(path, 'r').read())
			except:
				n = 0
			#ふぁぼ数を書き込み
			open(path, 'w').write(str(n+1))