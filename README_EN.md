日本語版 Readmeは[こちら](https://github.com/NephyProject/TwitterBotFramework/blob/master/README.md)です。

# TwitterBotFramework (TBFW)
Basic Concept: You can build your own Twitter-Bot in only little programming knowledge.

## Feature
### Easy to understand
Are you having only little programming knowledge? or Are you noob to programming?
<br>No problem!
<br>If you are use "TBFW", you can run your own Twitter bot yourself!!
<br>And, "TBFW" WROTE IN PYTHON! COMPILE IS NOT NEEDED! JUST RUN!!

### Useful
TBFW has logging feature. This feature will helpful to you! (e.g. Plugin load status, Exception status...)
<br>And, TBFW has JSON API too! Json API will give to you internal status (e.g. Threads)
<br>**If you encountered to any bugs, Please post your log to issue if possible!**

### Many
TBFW supporting multiple Twitter account.
<br>TBFW working with multi-thread, this mean work independently each account.

### Make it yourself
TBFW can add any feature with plugin.
<br>if you want make plugin, please see this [Wiki](https://github.com/NephyProject/TwitterBotFramework/wiki/%5B%E3%83%97%E3%83%A9%E3%82%B0%E3%82%A4%E3%83%B3%5D%E4%BB%95%E6%A7%98) (Wiki is not l18n to English...)

### Freely
This project published under MIT LICENSE.
<br>You can use this with no cost, no limit!
<br>For example, You can make bot using TBFW and publish the your code.

## How to Install (on CentOS 7)
TBFW working at Python 3.2 or higher.

### 1. Clone Repository
```bash
cd ~
git clone git@github.com:NephyProject/TwitterBotFramework.git
```

### 2. Install Library used by TBFW
```bash
cd TwitterBotFramework
pip install -r requirements.txt
```

### 3. Create `Config.json`
Copy `sample.config.json` and edit it.

|Option Name|Description|Required?|Default value|
|:-----------:|:------------:|:-----------:|:------------:|
|accounts|Account array used by TBFW|Yes|-|
|muteClient|Name of igone client(via). assign using array|No|[]|
|muteUser|ScreenName of igone user. assign using array|No|[]|
|muteDomain|Domain of igone URL. assign using array|No|[]|

The following are options in `accounts` array.

|Option Name|Description|Required?|Default value|
|:-----------:|:------------:|:-----------:|:------------:|
|id|Account's Numeric ID.|Yes|-|
|ck|Account's Consumer Key.|Yes|-|
|cs|Account's Comsumer Secret.|Yes|-|
|at|Account's Access Token.|Yes|-|
|ats|Account's Access Token Secret.|Yes|-|
|sn|Account's ScreenName.|Yes|-|
### 4. Run
```bash
python3 main.py
```
