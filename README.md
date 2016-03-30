# TwitterBot_Framework
Only little knowledge in programming, you can run Twitter Bot.

プログラミングの経験がない人やプログラムに疎い人でも、簡単にTwitter Botが自前で構築できるよう、設計されています。

##導入
###1. Pythonのインストール
<del>Python 3.x系でも動作するコードですが、Python 2.7.x系の導入をおすすめします。</del><br>
`Commit: e6c866be10ed435784d3ed94b79b73a2cbb8fcd2`からPython 3へ[完全移行](https://github.com/NephyProject/TwitterBot_Framework/commit/e6c866be10ed435784d3ed94b79b73a2cbb8fcd2)しました。Python 2.7.x系では**動作しません**のでご注意ください。

最新のPython 3.5.1は[こちら](https://www.python.org/downloads/release/python-351/)でダウンロードできます。
###2. パッケージ管理システム`pip`のインストール
`sudo curl -kL https://bootstrap.pypa.io/get-pip.py | python`
###3. TwitterBot_Frameworkで使用しているライブラリのインストール
`pip install tweepy yaml watchdog`
>複数のバージョンのPythonがインストールされている場合、`pip`ではなく`pip3.5`などのように`pip`の直後にバージョン番号が入ることがあります。
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
```bash
mkdir data
mkdir logs
```
###7.実行
```bash
cd TwitterBot_Framework
python Main.py &
```

##プラグイン開発
プラグインの[ドキュメント](https://github.com/NephyProject/TwitterBot_Framework/wiki/%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%E9%96%8B%E7%99%BA)をご覧ください。
