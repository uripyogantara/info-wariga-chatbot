import sys, re
import time
import telepot
import uuid
import json
import mysql.connector as mc
import pymysql

from connector import connector

def in_tele(msg):
    # proses 2
    imagefile_path = 'assets/'
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    # pesan = str(pesan).replace("'", "")
    # pesan = str(pesan).replace("\\", "")
    abaikan = 0
    if(content_type == 'document'):
        mime_type = msg['document']['mime_type']
        if (mime_type == 'image/jpeg' or mime_type == 'image/png' or mime_type == 'application/pdf'):
            ext = mime_type.split('/')[1]
            file_id = msg['document']['file_id']
            random_name = str(uuid.uuid4().hex)
            filename = imagefile_path + str(chat_id) + '_' + random_name + '.' + str(ext)
            print('file: ', filename)
            bot.download_file(file_id, filename)
            pesan = filename

        else:
            # print('format file tidak diijinkan')
            abaikan = 1
            pass
    elif(content_type == 'photo'):
        ext = 'png'
        file_id = msg['photo'][-1]['file_id']
        random_name = str(uuid.uuid4().hex)
        filename = imagefile_path + str(chat_id) + '_' + random_name + '.' + str(ext)
        print('file: ', filename)
        bot.download_file(file_id, filename)
        pesan = filename
        # bot.download_file(msg['photo'][-1]['file_id'], './file.png')
    elif (content_type == 'location'):
        # pesan = json.dumps(msg['location'])
        # pesan = pesan.replace("'", '"')
        pesan = str(msg['location']['latitude']) + '###' + str(msg['location']['longitude'])

    else:
        pesan = msg['text'].lower()

    if (abaikan == 0):
        print(chat_id, pesan)

        done = False
        print(chat_id, pesan)
        while not done:
            try:
                cur.execute("""INSERT INTO tb_inbox (chat_id, in_msg) VALUES ("%s", "%s")""" %
                            (chat_id, pesan))
                conn.commit()
                done = True
            except:
                conn.reconnect(attempts=1, delay=0)
                print("db mati, reconnect..")
    print(content_type, chat_type, chat_id, msg['message_id'])

# TOKEN = '309632028:AAFa8OJGIVxHVjSknyG2STClycnUxbjKS5Y'
#TOKEN = '376233101:AAE0FDKgUEidCPl70hAytDJH4iOJYoZHv1M'
TOKEN = '334319930:AAHyjQ77hFV73RazU6pUwtSoOvJRBZVSfcg' #light bot
# TOKEN ='627806342:AAH6IhM-sI-tQqmJgxhsJ1Js-9nAxLWpeS0'
# pertama kali

bot = telepot.Bot(TOKEN)
bot.message_loop(in_tele)
print('listen')

conn = connector().get_connection_object()
cur = conn.cursor()
while 1:
    time.sleep(1)