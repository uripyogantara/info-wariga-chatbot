import sys
import time
import telepot
import pymysql
import mysql.connector as mc
from connector import connector

def sendFileMsg(fname, chat_id):
    doc = open(fname,'rb')
    # send = bot.send_document(chat_id, doc)
    bot.sendDocument(chat_id, doc)

def sendImg(fname, chat_id):
    doc = open(fname,'rb')
    # send = bot.send_document(chat_id, doc)
    bot.sendPhoto(chat_id, doc)

def sendLoc(out_msg, chat_id):
    latitude, longitude = out_msg.split('###')
    bot.sendLocation(chat_id, latitude, longitude)

def out_tele():
    conn.commit()
    # cur.execute("SELECT * FROM tb_outbox WHERE flag='1'")
    cur.execute("SELECT * FROM tb_outbox WHERE flag='1'")
    for row in cur.fetchall():
        chat_id = row[2]
        out_msg = row[3]
        msg_type = row[4]
        try:
            if msg_type == 'msg':
                pesan = bot.sendMessage(chat_id, out_msg)
                print(pesan)
            elif msg_type == 'img':
                sendImg(out_msg, chat_id)
            elif msg_type == 'loc':
                sendLoc(out_msg, chat_id)
            else:
                sendFileMsg(out_msg, chat_id)
        except:
            print("send error")
        cur.execute("UPDATE tb_outbox SET flag='2' WHERE id_outbox='%s'" % row[0])
        conn.commit()
    conn.rollback()


if __name__ == '__main__':
    TOKEN = 'TOKEN' #light bot
    bot = telepot.Bot(TOKEN)
    print('Reading ...')

    conn = connector().get_connection_object()
    cur = conn.cursor()

    while 1:
        try:
            out_tele()
            time.sleep(1)
        except:
            conn.reconnect(attempts=1, delay=0)
            print("exception, reconnect")