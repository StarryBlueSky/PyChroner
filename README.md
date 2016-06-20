English readme is [here](https://github.com/NephyProject/TwitterBotFramework/blob/master/README_EN.md).


# TwitterBotFramework (TBF)
基本理念: プログラムの知識の少ない人でも簡単にボットを建てられるようにする。  

プログラミングの経験がない人やプログラムに疎い人でも、TBFを使えば、簡単にTwitter Botが自前で構築できるよう、設計されています。  
また、TBFでは安易に機能を追加できます。末尾をご覧ください。  

TBFを導入するにあたり、以下の操作が必要です。操作は簡単です。  

## 導入
### 1. Pythonのインストール
~~Python 3.x系でも動作するコードですが、Python 2.7.x系の導入をおすすめします。~~   
`Commit: e6c866be10ed435784d3ed94b79b73a2cbb8fcd2`からPython 3.x系へ[完全移行](https://github.com/NephyProject/TwitterBot_Framework/commit/e6c866be10ed435784d3ed94b79b73a2cbb8fcd2)しました。Python 2.7.x系では**動作しません**のでご注意ください。  

執筆当時、最新のPython 3.5.1は[こちら](https://www.python.org/downloads/release/python-351/)でダウンロードできます。  

### 2. パッケージ管理システム`pip`のインストール Installing PIP (Python Packaging System)
```bash
sudo curl -kL https://bootstrap.pypa.io/get-pip.py | python
```
### 3. TwitterBot_Frameworkで使用しているライブラリのインストール
```bash
pip install tweepy pyYAML watchdog
```
>複数のバージョンのPythonがインストールされている場合、`pip`ではなく`pip3.5`などのように`pip`の直後にバージョン番号が入ることがあります。

### 4. Twitterアプリケーション取得 (既存のConsumer Key/Secretを使う場合はスキップ)
[こちら](https://apps.twitter.com/app/new)で作成できます。ただし、携帯の電話番号の登録が必要である可能性があります。  

### 5. 設定を変更
初期状態では`setting.yaml`に設定を書き込んでください。ただし、全角スペースやタブを使用すると正しく認識されないのでご注意ください。代わりに半角スペースを使用してください。  

`SCREEN_NAME`: Botのスクリーンネーム(@~~)

`CONSUMER_KEY`: Consumer Key

`CONSUMER_SECRET`: Consumer Secret

`ACCESS_TOKEN`: Access Token

`ACCESS_TOKEN_SECRET`: Access Token Secret

`PLUGIN_DIR`: プラグインの保管場所を指定(デフォルト: plugins)

`WORK_DIR`: Botの作業用ディレクトリを指定(デフォルト: data)

`LOG_DIR`: ログを保管する場所を指定(デフォルト: logs)

### 6. 5で設定したディレクトリをつくる
```bash
mkdir data
mkdir logs
```
### 7. 実行
```bash
cd TwitterBot_Framework
python Main.py &
```

## プラグイン開発
TBFでは、簡単に機能を追加できます。プラグインの製作方法は以下を参照してください。  
プラグインの[仕様編](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E4%BB%95%E6%A7%98) および [引数編](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E5%BC%95%E6%95%B0)をご覧ください。  

