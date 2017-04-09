# sopel-telegram-gateway

Telegram group chat gateway for Sopel IRC bot, supports images and bi-directional messages.

## Setup

First, you'll need to have [Sopel IRC bot](https://sopel.chat/) and [Telepot library](https://github.com/nickoala/telepot) installed (see requirements.txt). You can use pip to install them.

Second, you'll need to create a Telegram bot with @BotFather on Telegram. Third, you'll have to change the privacy 
setting with /setprivacy to enable bot to see messages on the chat. Fourth, add the bot to the chat you want to.

To add this module to Sopel, copy telegram.py to ~/.sopel/modules and configure the module in ~/.sopel/default.cfg:

```
[telegram]
token = place your telegram bot token here
chat_id = place chat id here to send messages to (see below)
images = true
image_directory = /path/to/save/images/to
url_prefix = http://url/to/prepend/
```

To find out the chat ID, you can use the simple tool (find_chatid.py) with your token to list all your chats.
Run the tool and give the bot token as the first parameter. Now, send a messages to the chat and you should
see the chat ID (integer, can be negative).

## Limitations

1. The module will send messages to all IRC channels that the bot is joined to. 
2. There is no cleanup for images (hint: use tmpwatch).
3. There is no remapping of nicks, Telegram nick is used as-is.
