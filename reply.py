from nlp import nlp
import time
from connector import connector
import random
import string
import requests

def main():
    cursor.execute("SELECT * FROM tb_inbox WHERE flag='1'")
    inboxes = cursor.fetchall()
    # print(inboxes)

    for inbox in inboxes:
        # print(inbox)


        replies = nlp.get_reply(inbox["in_msg"])
        id_inbox = inbox["id_inbox"]
        chat_id = inbox["chat_id"]

        if inbox["in_msg"]=='/start':
            replies.append(generate_username(inbox))

        if len(replies)>0:
            for reply in replies:
                cursor.execute("INSERT INTO tb_outbox (id_inbox,chat_id, out_msg) VALUES ('%d', '%d','%s')" % (
                id_inbox, chat_id, reply))
                connection.commit()
                print("%d -> %s" % (chat_id, reply))
        else:
            cursor.execute("INSERT INTO tb_outbox (id_inbox,chat_id, out_msg) VALUES ('%d', '%d','%s')" % (
                id_inbox, chat_id, "Mohon maaf saya kurang tau"))
            connection.commit()
        cursor.execute("UPDATE tb_inbox SET flag='0' WHERE id_inbox='%s'" % inbox["id_inbox"])
        connection.commit()
        # print(reply)
    connection.rollback()

def generate_username(inbox):
    print("generrate user")
    print(inbox)
    cursor.execute("SELECT * FROM tb_user where chat_id=%s"%inbox['chat_id'])
    user=cursor.fetchone()
    print(user)
    username=user['username']
    if username is None:
        username = (user['first_name'] + user['last_name']).lower()
        digit=''.join(random.choice(string.digits) for i in range(2))
        username=username+digit
    password=randomStringDigits(6).lower()
    print(username,password)
    payload = {'username': username, 'password': password}
    url="http://localhost:8000/api/user/%s/verify"%user['verified_token']
    r = requests.put(url, params=payload)

    msg="Anda dapat mengakses melakukan login pada web melalui link http://infowariga.com\n" \
        "username\t: %s \n" \
        "password\t: %s"%(username,password)
    return msg
    # else

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
if __name__== "__main__":
    connection = connector().get_connection_object()
    cursor = connection.cursor(dictionary=True)
    nlp = nlp()

    while 1:
        main()
        time.sleep(1)