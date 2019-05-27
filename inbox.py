import time
import telepot
import string
import random
from telepot.loop import MessageLoop
from connector import connector
from pprint import pprint

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    user=msg['from']
    # print(user)

    insert_user(user['id'],user['first_name'],user['last_name'],user['username'])

    if content_type == 'text':
        pesan = msg['text'].lower()

        done=False

        while not done:
            try:
                cursor.execute("INSERT INTO tb_inbox (chat_id, in_msg) VALUES ('%s', '%s')" %
                               (chat_id, pesan))
                connection.commit()
                # print(content_type, chat_type, chat_id, msg['message_id'])
                done=True
            except:
                connection.reconnect(attempts=1, delay=0)
                print("exception, reconnect")

def insert_user(id,first_name,last_name,username):
    done=False

    while not done:
        try:
            cursor.execute("SELECT * FROM `tb_user` where chat_id=%d"%id)
            user=cursor.fetchone()
            print(user)
            if user is None:
                cursor.execute("INSERT INTO `tb_user` (chat_id,first_name,last_name,username,verified_token) VALUES (%d,'%s','%s','%s','%s')"%(id,first_name,last_name,username,randomStringDigits(50)))
                connection.commit()
                print("inserted")
            connection.rollback()
            done=True
        except:
            connection.reconnect(attempts=1, delay=0)
            print("exception, reconnect")
def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

if __name__ == '__main__':
    TOKEN = '796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY'
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()
    connection = connector().get_connection_object()
    cursor = connection.cursor(dictionary=True)
    print ('Listening ...')
    # Keep the program running.
    while 1:
        time.sleep(10)

