import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from mysql.connector import Error
import time

master_con=mysql.connector.connect(host='localhost',database='chatbot_master',user='root',password='')
cursor_master=master_con.cursor(dictionary=True)

cursor_master.execute("SELECT * FROM master_host")

hosts=cursor_master.fetchall()
# con=[]
def xstr(data):
    if data is None:
        return ''
    else:
        return str(data)

def main():
    for host in hosts:
        connection_pool= mysql.connector.pooling.MySQLConnectionPool(pool_name="info_wariga",
                                                          pool_reset_session=True,
                                                         host=host['ip'],
                                                         user=host['user'],
                                                         passwd="",
                                                         database=host['nama_db'],)
        con =connection_pool.get_connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_antrean WHERE flag='1'")
        antrean=cursor.fetchall()

        for antrean_item in antrean:
            print(host['nama_db'],antrean_item)

            for host2 in hosts:
                connection_pool2 = mysql.connector.pooling.MySQLConnectionPool(pool_name="info_wariga",
                                                                              pool_reset_session=True,
                                                                              host=host2['ip'],
                                                                              user=host2['user'],
                                                                              passwd="",
                                                                              database=host2['nama_db'], )

                con2 = connection_pool2.get_connection()
                cursor2 = con2.cursor(dictionary=True)
                cursor2.execute("SELECT * FROM tb_inbox WHERE flag IN ('1','2','3')")
                data=cursor2.fetchall()
                print(host2['nama_db'],len(data),host2['batas_atas'])

                if len(data)<host2['batas_atas']:
                    sql="INSERT INTO tb_inbox (chat_id, in_msg) VALUES (%s, %s)"
                    data=(
                        antrean_item["chat_id"],
                        antrean_item["in_msg"],
                    )
                    cursor2.execute(sql,data)
                    con2.commit()
                    print("insert")

                    update="UPDATE tb_antrean SET flag='4' where id_inbox=%d"%antrean_item['id_inbox']
                    print(update)
                    cursor.execute(update)
                    con.commit()

if __name__ == '__main__':
    while True:
        main()
        print("check")
        time.sleep(30)

