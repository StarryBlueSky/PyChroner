# TwitterBotFramework (TBF)
基本理念: プログラムの知識の少ない人でも簡単にボットを建てられるようにする。
Basic Concept: Only little knowledge in programming, you can build Twitter-Bots.

プログラミングの経験がない人やプログラムに疎い人でも、TBFを使えば、簡単にTwitter Botが自前で構築できるよう、設計されています。<br>
This TBF is designed so that even people who are NOT familir with programming can build their own bots.<br>
また、TBFでは安易に機能を追加できます。末尾をご覧ください。<br>
And, this TBF allows you to add original features easily. Please check about it below this page.

TBFを導入するにあたり、以下の操作が必要です。操作は簡単です。<br>
There are a few operations to have to do. Operations are easy. Check below.

##導入 Introduction
###1. Pythonのインストール Installing Python
<del>Python 3.x系でも動作するコードですが、Python 2.7.x系の導入をおすすめします。</del><br>
`Commit: e6c866be10ed435784d3ed94b79b73a2cbb8fcd2`からPython 3.x系へ[完全移行](https://github.com/NephyProject/TwitterBot_Framework/commit/e6c866be10ed435784d3ed94b79b73a2cbb8fcd2)しました。Python 2.7.x系では**動作しません**のでご注意ください。
<del>This code can be runable on Python 3.x, but you should install Python 2.7.x.</del><br>
From `Commit: e6c866be10ed435784d3ed94b79b73a2cbb8fcd2`[Link](https://github.com/NephyProject/TwitterBot_Framework/commit/e6c866be10ed435784d3ed94b79b73a2cbb8fcd2), This TBF is fully compatible with Python 3.x. Be careful! No longer this TBF is incompatible with Python 2.7.x.

執筆当時、最新のPython 3.5.1は[こちら](https://www.python.org/downloads/release/python-351/)でダウンロードできます。<br>
Latest Python 3.5.1 is [here](https://www.python.org/downloads/release/python-351/).
###2. パッケージ管理システム`pip`のインストール Installing PIP (Python Packaging System)
`sudo curl -kL https://bootstrap.pypa.io/get-pip.py | python`
###3. TwitterBot_Frameworkで使用しているライブラリのインストール Installing some libraries
`pip install tweepy pyYAML watchdog`
>複数のバージョンのPythonがインストールされている場合、`pip`ではなく`pip3.5`などのように`pip`の直後にバージョン番号が入ることがあります。

>You may have to install libraries with `pip3.5`. This is because your system has Python 3.5.

###4. Twitterアプリケーション取得 (既存のConsumer Key/Secretを使う場合はスキップ) Creating OAuth Application
[こちら](https://apps.twitter.com/app/new)で作成できます。ただし、携帯の電話番号の登録が必要である可能性があります。<br>
You can issue new application key from [here](https://apps.twitter.com/app/new).
###5. 設定を変更 Changing the Config
初期状態では`setting.yaml`に設定を書き込んでください。ただし、全角スペースやタブを使用すると正しく認識されないのでご注意ください。代わりに半角スペースを使用してください。<br>
Default config file is `setting.yaml`. Do NOT use tabs. Please use spaces.

`SCREEN_NAME`: Botのスクリーンネーム(@~) Bot's Twitter ScreenName

`CONSUMER_KEY`: Consumer Key

`CONSUMER_SECRET`: Consumer Secret

`ACCESS_TOKEN`: Access Token

`ACCESS_TOKEN_SECRET`: Access Token Secret

`PLUGIN_DIR`: プラグインの保管場所を指定(デフォルト: plugins) The path of directory that has plugins.

`WORK_DIR`: Botの作業用ディレクトリを指定(デフォルト: data) The path of directory that is used for temp files.

`LOG_DIR`: ログを保管する場所を指定(デフォルト: logs) The path of directory that logs are written.
###6.5で設定したディレクトリをつくる Make Dirs that you're set up
```bash
mkdir data
mkdir logs
```
###7.実行 Execute
```bash
cd TwitterBot_Framework
python Main.py &
```

TBFでは、簡単に機能を追加できます。プラグインの製作方法は以下を参照してください。<br>
You can add features easily. You can learn about it below links.
##プラグイン開発 Developing Plugins
プラグインの[仕様編](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E4%BB%95%E6%A7%98) および [引数編](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E5%BC%95%E6%95%B0)をご覧ください。<br>
Plugin's [API](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E4%BB%95%E6%A7%98)<br>
Plugin's [Argument](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E5%BC%95%E6%95%B0)をご覧ください。
