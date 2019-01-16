import sys
import time
import telepot
import pymysql
import mysql.connector as mc

def sendFileMsg(fname, chat_id):
    doc = open(fname,'rb')
    # send = bot.send_document(chat_id, doc)
    bot.sendDocument(chat_id, doc)

def out_tele():
    conn.commit()
    cur.execute("SELECT * FROM tb_outbox WHERE flag='1'")
    for row in cur.fetchall():
        chat_id = row[2]
        out_msg = row[3]
        msg_type = row[4]

        if msg_type == 'msg':
            pesan = bot.sendMessage(chat_id, out_msg)
            print(pesan)
        else:
            sendFileMsg(out_msg, chat_id)

        cur.execute("UPDATE tb_outbox SET flag='2' WHERE id_outbox='%s'" % row[0])
        conn.commit()


TOKEN ='6eS0'
bot = telepot.Bot(TOKEN)
print ('Reading ...')

while 1:
    try:
        conn = mc.connect(host='localhost', user='root', passwd='root', db='mca')
        cur = conn.cursor()
    except:
        print('db mati')

    out_tele()
    time.sleep(1)