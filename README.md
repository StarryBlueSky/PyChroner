English README is [here](https://github.com/NephyProject/PyChroner/blob/master/README_EN.md).

# PyChroner: Easy bot Framework
> Python + [Chronus](https://ja.wikipedia.org/wiki/%E3%82%AF%E3%83%AD%E3%83%8E%E3%82%B9_(%E6%99%82%E9%96%93%E3%81%AE%E7%A5%9E))(Cron) + er = PyChroner

[![Python](https://img.shields.io/badge/Python-3.6-blue.svg?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT%20License-blue.svg?style=flat-square)]()

基本理念: **Python初心者でも簡単にBotを運用できるようにする.**

重要なお知らせ: **TwitterBotFramework** は **PyChroner** に名称が変わりました.  
TwitterBotFrameworkの当初の目標(Goal)は, 既存のTwitter Bot作成サイト(twittbot.net, autotweety.net, ...)より柔軟で扱いやすいフレームワークを作る, ということでした.  
しかし, 現在では名称が旧称**TwitterBotFramework**から**PyChroner**に変更されたことからも分かるように, 今や作成可能なBotはTwitterの枠を超えています. 現状ではTwitter APIのほか, Discord APIに対応しており柔軟なBot作成が可能です.

## 動作確認環境
- Windows 10 Pro 64bit / Windows Server 2016 Datacenter 64bit / Ubuntu 17.01 64bit
- Python **3.6.0**以上

ただし, Windows NT系ではPluginのTimeout機能は利用できません. 詳細は`PluginAPI`の項でご確認ください.

## 特徴
準備中.

## 導入方法
以下では, Python 3.6.1がインストール済みとしています.

このリポジトリをCloneし, sample.config.jsonを参考に設定値を変更します. 詳しくは[設定リファレンス](https://github.com/NephyProject/PyChroner/wiki/config.json-Reference)をご覧ください.  
設定を更新したら `python main.py`を実行すればPyChronerは立ち上がります.

起動することを確認したら, プラグインを`plugins`内に配置しましょう. 想像力次第でなんでもできます.

## ライセンス
PyChronerは, [MITライセンス](https://github.com/NephyProject/PyChroner/wiki/LICENSE) の下で公開されています.  
このライセンスの下では, 誰でも自由に無料でPyChronerを使用, 改造, 再配布, 商用利用が許可されます.

Copyright © 2017 Nephy Project Team.  
