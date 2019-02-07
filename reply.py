from nlp import nlp
import time
from connector import connector

def main():
    cursor.execute("SELECT * FROM tb_inbox WHERE flag='1'")
    inboxes = cursor.fetchall()
    # print(inboxes)

    for inbox in inboxes:
        # print(inbox)
        replies = nlp.get_reply(inbox["in_msg"])
        #
        # print(replies)
        id_inbox = inbox["id_inbox"]
        chat_id = inbox["chat_id"]
        for reply in replies:
            cursor.execute("INSERT INTO tb_outbox (id_inbox,chat_id, out_msg) VALUES ('%d', '%d','%s')" % (
            id_inbox, chat_id, reply))
            connection.commit()
            print("%d -> %s" % (chat_id, reply))

        cursor.execute("UPDATE tb_inbox SET flag='2' WHERE id_inbox='%s'" % id_inbox)
        connection.commit()
        # print(reply)
    connection.rollback()

if __name__== "__main__":
    connection = connector().get_connection_object()
    cursor = connection.cursor(dictionary=True)
    nlp = nlp()

    while 1:
        main()
        time.sleep(1)