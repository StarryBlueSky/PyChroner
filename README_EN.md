# TwitterBotFramework (TBF)
Basic Concept: Only little knowledge in programming, you can build Twitter-Bots.

This TBF is designed so that even people who are NOT familir with programming can build their own bots.  
And, this TBF allows you to add original features easily. Please check about it below this page.


There are a few operations to have to do. Operations are easy. Check below.

## Introduction

### 1. Installing Python
~~This code can be runable on Python 3.x, but you should install Python 2.7.x.~~  
From [`Commit: e6c866be10ed435784d3ed94b79b73a2cbb8fcd2`](https://github.com/NephyProject/TwitterBot_Framework/commit/e6c866be10ed435784d3ed94b79b73a2cbb8fcd2), This TBF is fully compatible with Python 3.x. Be careful! No longer this TBF is incompatible with Python 2.7.x.

Latest Python 3.5.1 is [here](https://www.python.org/downloads/release/python-351/).

### 2. Installing `pip` (Python Packageing System)
```bash
sudo curl -kL https://bootstrap.pypa.io/get-pip.py | python
```

### 3. Installing some libraries
```bash
pip install tweepy pyYAML watchdog
```

>You may have to install libraries with `pip3.5`. This is because your system has Python 3.5.

### 4. Creating OAuth Application
You can create new application key from [here](https://apps.twitter.com/app/new).

### 5. Changing the Config
Default config file is `setting.yaml`. Do NOT use tab indent. Please use space indent.

`SCREEN_NAME`: Bot's Twitter ScreenName (@~~)

`CONSUMER_KEY`: Consumer Key

`CONSUMER_SECRET`: Consumer Secret

`ACCESS_TOKEN`: Access Token

`ACCESS_TOKEN_SECRET`: Access Token Secret

`PLUGIN_DIR`: The path of directory that has plugins. (Default: `plugins`)

`WORK_DIR`: The path of directory that is used for temp files. (Default: `data`)

`LOG_DIR`: The path of directory that logs are written. (Default: `logs`)

### 6. Make dirs that you've set up
```bash
mkdir data
mkdir logs
```
### 7. Execute
```bash
cd TwitterBot_Framework
python Main.py &
```

## Developing Plugins
You can add features easily. You can learn about it below links.  
(**Important!** Those documents are *not* l18n to English.)  

Plugin's [API](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E4%BB%95%E6%A7%98)  
Plugin's [Argument](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E5%BC%95%E6%95%B0)

