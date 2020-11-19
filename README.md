# telepyd
An easy-to-use bot for telegram based on [python-droit](https://github.com/jarinox/python-droit/) and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/).  
  
Customize your bot using the Droit Database Script - question-to-answer rules are defined that simple:

```
TELE*cmd!start->Welcome to the telepyd bot.
SRTX!how are you->TEXT!I'm fine.
```
The integrated telegram-plugins make it possible to display `InlineKeyboards`.  

Just have a look at `data/bot.dda`. If you aren't familiar with Droit Database Script you can learn about it by reading "[an introduction to Droit v1.1](https://github.com/jarinox/python-droit/wiki/Introduction-to-Droit-v1.1#Droit-Database-Script)".

## Installation
Download or clone this repository.  
```
git clone https://github.com/jarinox/telepyd.git
cd telepyd
```
and install the requirements from `requirements.txt`
```
pip install -r requirements.txt
```

## Setup
Rename the file `data/config.sample.json` to `data/config.json` and insert your token. You can get a token using [BotFather](https://core.telegram.org/bots#6-botfather). If you want to change the name of your bot or disable logging you can adjust those settings too.

## Running your bot
Open the `telepyd` folder with your terminal and run:  
```
python3 telepyd.py
```

[This wiki entry](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Hosting-your-bot) from python-telegram-bot explains how to host your bot.  