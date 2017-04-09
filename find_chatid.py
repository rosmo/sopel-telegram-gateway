import sys
import time
import telepot
import telepot.namedtuple

# Based on emodi.py from Telepot samples

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    if chat_id < 0:
        print 'Received a %s from %s, by %s, chat ID %s' % (content_type, m.chat, m.from_, chat_id)
    else:
        print 'Received a %s from %s, chat ID %s' % (content_type, m.chat)

TOKEN = sys.argv[1] 

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print 'Listening for messages on chat...'

while 1:
    time.sleep(10)
