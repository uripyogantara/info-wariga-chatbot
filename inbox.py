import sys
import time
import telepot
import pymysql
import mysql.connector as mc

def in_tele(msg):
    # proses 2
    content_type, chat_type, chat_id = telepot.glance(msg)
    pesan = msg['text'].lower()
    print(chat_id,pesan)
    cur.execute("INSERT INTO tb_inbox (chat_id, in_msg) VALUES ('%s', '%s')" %
                (chat_id, pesan))
    conn.commit()
    print(content_type, chat_type, chat_id, msg['message_id'])


TOKEN ='62'
# pertama kali
bot = telepot.Bot(TOKEN)
bot.message_loop(in_tele)
print('listen')

while 1:
    try:
        # proses 1
        conn = mc.connect(host='localhost', user='root', passwd='', db='mca')
        cur = conn.cursor()
    except:
        print('db mati')

    time.sleep(1)