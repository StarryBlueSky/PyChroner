English Readme is [here](https://github.com/NephyProject/TwitterBotFramework/blob/master/README_EN.md).

# TwitterBotFramework (TBFW)
基本理念: **プログラムの知識の少ない人でも簡単にTwitter Botを運用できるようにする。**

## 特徴
### わかりやすく
プログラミングの経験がない人や疎い人でも TBFWを使えば 簡単にTwitter Botが自前で構築できるよう、設計されています。
<br>また、Pythonで書かれているため実行前にコンパイルは不要です。

### べんりに
TBFWは ロギング機能を有しています。このため、プラグインのロード状況や 例外の発生などを容易に確認できます。
<br>また、JSONにて内部の状況(スレッド等)を吐き出すAPIも整備されています。
<br>バグを見つけたと思われる際にはissueにログを掲載してくださると助かります。

### いっぱい
TBFWは 複数のTwitterアカウントに対応しています。
<br>TBFWは マルチスレッドで動作するのでそれぞれのアカウントが独立して処理されるため、動作に支障は出ません。

### おもいのままに
TBFWは プラグインシステムを用いて簡単に機能を追加できます。
<br>実際にプラグインを開発するには Wikiの[プラグインの仕様まとめ](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E4%BB%95%E6%A7%98)をご覧ください。  

### じゆうに
このプロジェクトは MITライセンスで公開されています。
<br>したがって、だれでも無償で無制限に利用できます。
<br>例えば、このTBFWを利用してBotを作成して 実際に稼働させたりそのソースコードを公開したりすることも自由にできます。

## 導入方法 (CentOS 7での例)
TBFWは Python 3.5.1までのPython 3.xで動作します。

### 1. リポジトリのクローン
```bash
cd ~
git clone git@github.com:NephyProject/TwitterBotFramework.git
```

### 2. TBFWで使用しているライブラリのインストール
```bash
cd TwitterBotFramework
pip install -r requirements.txt
```

### 3. `config.json`の作成
`sample.config.json`をコピーして編集してください。

|オプション名|説明|必須?|デフォルト値|
|:-----------:|:------------:|:-----------:|:------------:|
|accounts|TBFWで使用するアカウントの配列です|Yes|-|
|muteClient|無視するクライアント(via)の名称です。配列で指定します。|No|[]|
|muteUser|無視するユーザーのスクリーンネームです。配列で指定します。|No|[]|
|muteDomain|無視するドメインです。配列で指定します。|No|[]|

以下は`accounts`配列内のオプションです。

|オプション名|説明|必須?|デフォルト値|
|:-----------:|:------------:|:-----------:|:------------:|
|id|アカウントの数字IDです。|Yes|-|
|ck|アカウントのConsumer Keyです。|Yes|-|
|cs|アカウントのComsumer Secretです。|Yes|-|
|at|アカウントのAccess Tokenです。|Yes|-|
|ats|アカウントのAccess Token Secretです。|Yes|-|
|sn|アカウントのスクリーンネームです。|Yes|-|
### 4. 実行
```bash
python3 main.py
```
