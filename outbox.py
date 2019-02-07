import time
import datetime
import telepot
from connector import connector

def sendFileMsg(fname, chat_id):
    doc = open(fname,'rb')
    # send = bot.send_document(chat_id, doc)
    bot.sendDocument(chat_id, doc)

def out_tele():
    cursor.execute("SELECT * FROM tb_outbox WHERE flag='1'")

    for row in cursor.fetchall():
        chat_id = row["chat_id"]
        out_msg = row["out_msg"]
        msg_type = row["type"]

        if msg_type == 'msg':
            pesan = bot.sendMessage(chat_id, out_msg)
            print(pesan)
        else:
            sendFileMsg(out_msg, chat_id)

        try:
            cursor.execute("UPDATE tb_outbox SET flag='2' WHERE id_outbox='%s'" % row["id_outbox"])
            connection.commit()
        except:
            print("Error Update")
    connection.rollback()

if __name__ == '__main__':
    TOKEN = '796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY'
    bot = telepot.Bot(TOKEN)
    print('Reading ...')

    connection = connector().get_connection_object()
    cursor = connection.cursor(dictionary=True)
    while 1:
        try:
            out_tele()
            time.sleep(1)
        except:
            connection.reconnect(attempts=1, delay=0)
            print("exception, reconnect")
