import time
import telepot
from connector import connector


connection=connector().get_connection_object()
cursor = connection.cursor()

def sendFileMsg(fname, chat_id):
    doc = open(fname,'rb')
    # send = bot.send_document(chat_id, doc)
    bot.sendDocument(chat_id, doc)

def out_tele():
    cursor.execute("SELECT * FROM tb_outbox WHERE flag='1'")
    for row in cursor.fetchall():
        chat_id = row[2]
        out_msg = row[3]
        msg_type = row[4]

        if msg_type == 'msg':
            pesan = bot.sendMessage(chat_id, out_msg)
            print(pesan)
        else:
            sendFileMsg(out_msg, chat_id)

        cursor.execute("UPDATE tb_outbox SET flag='2' WHERE id_outbox='%s'" % row[0])
        connection.commit()
    connection.rollback()


TOKEN ='796693170:AAFb0M0YAuRMJgz83eus-Qfv_uPDgR5BKUY'
bot = telepot.Bot(TOKEN)
print ('Reading ...')

while 1:
    out_tele()
    time.sleep(1)