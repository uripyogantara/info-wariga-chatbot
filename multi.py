import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from mysql.connector import Error
import time
from mojodomo import mojodomo

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
    for host in hosts:
        data=mojodomo(host)
        data.get_antrean(antrean)
        # print("before distribute",antrean)
        # data.distribute(antrean)
        # print("after distribute",antrean)


def store_antrean():
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
    antrean = []
    while True:
        main()
        print("check",antrean)
        store_antrean()
        time.sleep(2)

