import time
import telepot
from telepot.loop import MessageLoop
from connector import connector

connection=connector().get_connection_object()
cursor = connection.cursor()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # pprint(msg)

    if content_type == 'text':
        pesan = msg['text'].lower()
        print(chat_id, pesan)

        done=False

        while not done:
            try:
                cursor.execute("INSERT INTO tb_inbox (chat_id, in_msg) VALUES ('%s', '%s')" %
                               (chat_id, pesan))
                connection.commit()
                print(content_type, chat_type, chat_id, msg['message_id'])
                done=True
            except:
                connection.reconnect(attempts=1, delay=0)
                print("exception, reconnect")

TOKEN = '796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY'
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)