import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from mysql.connector import Error
import time
from antrean import antrean

master_con=mysql.connector.connect(host='localhost',database='chatbot_master',user='root',password='')
cursor_master=master_con.cursor(dictionary=True)

cursor_master.execute("SELECT * FROM master_host")
hosts=cursor_master.fetchall()


def xstr(data):
    if data is None:
        return ''
    else:
        return str(data)

def main():
    global antrean
    for host in hosts:
        data=antrean(host)
        antrean=data.get_antrean()
        print(host['id_host'], antrean)
        store_antrean(antrean)
        # print("before distribute",antrean)
        # data.distribute(antrean)
        # print("after distribute",antrean)


def store_antrean(antrean):
    for index, antrean_item in enumerate(antrean):
            sql = "INSERT INTO tb_inbox (chat_id, in_msg) VALUES (%s, %s)"
            # print("antrean item",antrean_item)
            data = (
                antrean_item["chat_id"],
                antrean_item["in_msg"],
            )

            cursor_master.execute(sql, data)
            master_con.commit()
if __name__ == '__main__':
    while True:
        main()
        # print("check",antrean)
        # store_antrean()
        time.sleep(2)

