# PyChroner

> Python + Chronus(Cron) = PyChroner  

基本理念: **プログラミングに疎い人でも簡単にBotを運用できるようにする。**  
English Readme is [here](/README_EN.md).  

お知らせ: **「TwitterBotFramework」は「PyChroner」に名前が変わりました。**
現在活発に **仕様及び機能の変更が行われている** ので、アップデートは必ず **変更点を確認してから** 行ってください。  
- [TwitterBotFrameworkからの大まかな変更点](https://github.com/NephyProject/PyChroner/wiki/changelog#v3)
- [TwitterBotFrameworkからのプラグイン移行ガイド](https://github.com/NephyProject/PyChroner/wiki/plugin_migration_fromTBFW)

## 特徴
### わかりやすく
プログラミングに疎い人でも、PyChronerを使えば、いろいろなBotがかんたんに構築できます。  
現在はTwitterのみを標準でサポートしていますが、将来的に各種サービスに対応する予定です。ごあんしんください。  

### べんりに
PyChronerはロギング機能を有しています。このため、プラグインのロード状況や、例外の発生などを容易に確認できます。  
また、JSONにて内部の状況(スレッド等)を吐き出すAPIも整備されています。  
バグを見つけたと思われる際にはissueにログを掲載してくださると助かります。  

### おもいのままに
PyChronerはプラグインシステムを用いて簡単に機能を追加できます。  
プラグインを作るには、Wikiの「[プラグインの作り方](https://github.com/NephyProject/PyChroner/wiki/plugin_getting_started)」をお読みください。  

### いっぱい
PyChronerはスペックの許す限りプラグインを読み込むことができます。  
プラグインはそれぞれが異なるスレッドで動作するため、一つのプラグインがその他のプラグインの動作に支障を与えることはありません。  

### じゆうに
このプロジェクトは MITライセンスで公開されており、ライセンスを遵守する限り自由に利用できます。  
例えば、このPyChronerをフォークして機能を追加したものを、同じMITライセンスでGitHub上に公開することなどが可能です。  

---

## 導入方法 (Redhat系)
PyChronerはバージョン**3.6**以上のPythonで動作します。

### 1. リポジトリのクローン
```bash
git clone https://github.com/NephyProject/PyChroner.git
```

### 2. 使用しているライブラリのインストール
```bash
cd PyChroner
sudo pip3 install watchdog timeout-decorator
```

### 3. `config.json`の作成
`sample.config.json`をコピーして編集してください。
```bash
cp sample.config.json
```
#### configの内容
|オプション名|説明|必須|デフォルト値|
|:-----------:|:------------:|:-----------:|:------------:|
|services|Botで使用する各種サービスのアカウント認証情報です。|Yes|-|
|logLevel|ログレベルの設定です。|Yes|info|
|slack|Slackへ通知するための各種設定です。|No|-|
|secret|プラグインにて使用する各種情報です。|No|-|

`services` での各種サービスアカウントの設定方法については、Wikiを参照してください。  
- [Twitterアカウントの設定](https://github.com/NephyProject/PyChroner/wiki/config_services_twitter)  

### 4. 実行
```bash
python3 main.py
```
初回起動時に `plugins` ディレクトリが生成されるので、その中にプラグインを入れると動作させることができます。  
エラーなどが発生した場合は `logs` 内のファイルに内容が記述されるため、そちらを参照してください。

---

## Copyright and License 
Copyright © 2017 Nephy Project Team All Rights Reserved.  
This product released under [The MIT License](/LICENSE).  
