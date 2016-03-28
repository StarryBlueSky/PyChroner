# TwitterBot_Framework
Only little knowledge in programming, you can run Twitter Bot.

プログラムの知識が疎い人でも、簡単にTwitter Botが自前で構築できるよう、設計されています。

##導入
###1. Python 2.7.xのインストール
最新のPython 2.7.11は[こちら](https://www.python.org/downloads/release/python-2711/)でダウンロードできます。
###2. パッケージ管理システム`pip`のインストール
`sudo curl -kL https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python`
###3. TwitterBot_Frameworkで使用しているライブラリのインストール
`pip install tweepy yaml`
###4. Twitterアプリケーション取得 (既存のConsumer Key/Secretを使う場合はスキップ)
[こちら](https://apps.twitter.com/app/new)で作成できます。ただし、携帯電話番号の登録が必要な模様。
###5. 設定を変更
初期状態では`setting.yaml`に設定を書き込んでください。ただし、タブを使用すると正しく認識されないのでご注意ください。

`SCREEN_NAME`: Botのスクリーンネーム(@~)

`CONSUMER_KEY`: 取得したConsumer Key

`CONSUMER_SECRET`: 取得したConsumer Secret

`ACCESS_TOKEN`: 4.のページで作成できるAccess Token

`ACCESS_TOKEN_SECRET`: 4.のページで生成できるAccess Token Secret

`PLUGIN_DIR`: プラグインの保管場所を指定(デフォルト: plugins)

`WORK_DIR`: Botの作業用ディレクトリを指定(デフォルト: data)

`LOG_DIR`: ログを保管する場所を指定(デフォルト: logs)
###6.5で設定したディレクトリをつくる
`mkdir data`

`mkdir logs`
###7.実行
`cd TwitterBot_Framework`

`python Main.py &`
