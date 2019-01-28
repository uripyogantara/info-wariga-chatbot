import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Ya', callback_data='ya')],
                    [InlineKeyboardButton(text='Tidak', callback_data='tidak')],
               ])

    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    if(query_data=="ya"):
        bot.answerCallbackQuery(query_id, text='Ya')
    elif(query_data=="tidak"):
        bot.answerCallbackQuery(query_id, text='Tidak')

TOKEN = "796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY"

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)