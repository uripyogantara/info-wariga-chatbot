import sys
import time
import telepot
from pprint import pprint
from telepot.loop import MessageLoop

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    pprint(msg)

    # if content_type == 'text':
    #     bot.sendMessage(chat_id, msg['text'])

bot= telepot.Bot("796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY")

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)