from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import commands, example, OP, rule, interval
from sopel.tools.time import (
    get_timezone, format_time, validate_format, validate_timezone
)
from sopel.config.types import StaticSection, ValidatedAttribute

import telepot
import telepot.namedtuple
import threading
import uuid
import base64

# Telegram-Sopel IRC bot gateway

class TelegramSection(StaticSection):
    token = ValidatedAttribute('token')
    chat_id = ValidatedAttribute('chat_id')
    images = ValidatedAttribute('images', bool, default=False)
    image_directory = ValidatedAttribute('image_directory')
    url_prefix = ValidatedAttribute('url_prefix')

def configure(config):
    config.define_section('telegram', TelegramSection)

def receive_from_telegram(msg):
    global message_queue
    
    message_queue.append(msg)

@interval(1)
def empty_message_queue(bot):
    global message_queue
    global message_lock
    global telegram

    if 'message_lock' not in globals():
        message_lock = threading.Semaphore()
    message_lock.acquire()

    for msg in message_queue:

        if 'text' in msg:
            message = '<%s> %s' % (msg['from']['username'], msg['text'])
            for channel in bot.channels:
                bot.say(message, channel, max_messages=2)

        if bot.config.telegram.images and 'photo' in msg:
            largest_photo = None
            for photo in msg['photo']:
                if not largest_photo or photo['file_size'] > largest_photo['file_size']:
                    largest_photo = photo

            if largest_photo:
                file_name = '%s.jpg' % (base64.urlsafe_b64encode(uuid.uuid4().bytes).replace('=', ''))
                file_path = '%s%s' % (bot.config.telegram.image_directory, file_name)
                file_url = '%s%s' % (bot.config.telegram.url_prefix, file_name)
                telegram.download_file(largest_photo['file_id'], file_path)
                
                for channel in bot.channels:
                    if 'caption' in msg and msg['caption']:
                        message = '<%s> %s: %s' % (msg['from']['username'], msg['caption'], file_url)
                    else:
                        message = '<%s> %s' % (msg['from']['username'], file_url)

                    bot.say(message, channel, max_messages=1)
                
        message_queue.remove(msg)

    message_lock.release()

def setup(bot):
    global telegram
    global message_queue

    message_queue = []

    bot.config.define_section('telegram', TelegramSection)

    telegram = telepot.Bot(bot.config.telegram.token)
    telegram.message_loop(receive_from_telegram)

@rule('.+')
def send_to_telegram(bot, trigger):
    global telegram

    telegram.sendMessage(int(bot.config.telegram.chat_id), '<%s> %s' % (trigger.nick, trigger))

