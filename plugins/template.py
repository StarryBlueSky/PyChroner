# -*- coding: utf-8 -*-
"""プラグインの適用先を指定 TARGET = ?
REPLY = リプライに対して適用されます
TIMELINE = タイムラインのツイートに対して適用されます
EVENT = UserStreamイベントに対して適用されます"""
TARGET = ''

"""実行確率 1/n RATIO = ?
n分の1でプラグインを実行します
必ず実行するには定義する必要はありません"""
RATIO = 1

"""関数名は必ずdoとして 1つの引数を受け取ること"""
def do(stream):
	"""引数について
	stream = UserStreamから受信したJSONの辞書オブジェクト

	中身についてはTwitterのドキュメントを確認のこと
	https://dev.twitter.com/rest/reference/get/statuses/show/%3Aid
	"""


	"""プラグインで実行する処理 詳しくは他の同梱プラグインを見て下さい"""


	"""エラーとして帰す場合は return Falseしてください
	ユーザーにコマンドの使い方を返します"""

	"""めかぞらるへの返り値について
	返り値には
	text(必須) = 返信したり投稿したりするツイート本文
	in_reply_to = リプライの場合に返信先のツイートID(Int)
	filename = 画像をアップロードする場合にファイルへの絶対パス (str)
	dm = TrueならDMで送信 Falseならツイートで送信
	lat = ツイートに付加する位置情報のうち、経度 int または float
	longs = ツイートに付加する位置情報のうち、緯度 int または float
	これらを辞書のKeyとValueにしてreturnしてください
	任意の返り値で指定がないものは自動的にNone(False)として代入されます"""
	text = None
	in_reply_to = None
	filename = None
	lat = None
	longs = None
	result = {"text": text, "in_reply_to": in_reply_to, "filename": filename, "dm": False, "lat": lat, "longs": longs}
	return result