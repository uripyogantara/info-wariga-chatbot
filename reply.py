import time
from connector import connector
from response import response

connection=connector().get_connection_object()
cursor = connection.cursor()
res = response()

def reply():
    cursor.execute("SELECT * FROM tb_inbox WHERE flag='1'")
    inboxes=cursor.fetchall()
    # print(inboxes)

    for inbox in inboxes:
        # print(inbox[2])
        replies=res.get_response(inbox[2])

        id_inbox=inbox[0]
        chat_id=inbox[1]
        for reply in replies:
            cursor.execute("INSERT INTO tb_outbox (id_inbox,chat_id, out_msg) VALUES ('%d', '%d','%s')" %(id_inbox,chat_id,reply ))
            connection.commit()
            print("%d -> %s"%(chat_id,reply))

        cursor.execute("UPDATE tb_inbox SET flag='2' WHERE id_inbox='%s'" % id_inbox)
        connection.commit()
        # print(reply)
    connection.rollback()


while 1:
    reply()
    time.sleep(1)