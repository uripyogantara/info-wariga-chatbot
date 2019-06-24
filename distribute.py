import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from mysql.connector import Error
import time
from antrean import antrean
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mojodomo",
                                                              pool_reset_session=True,
                                                              host='localhost',
                                                              database='chatbot_master',
                                                              user='root',
                                                              password='')
connection=connection_pool.get_connection()
cursor=connection.cursor(dictionary=True)

cursor.execute("SELECT * FROM master_host")
hosts=cursor.fetchall()

def distribute_message():
    cursor.execute("SELECT * FROM tb_inbox WHERE flag='1'")
    antrean=cursor.fetchall()
    for host in hosts:
        data = antrean(host)
        id_inbox=data.distribute(antrean)
        update_inbox(id_inbox)
    connection.rollback()

def update_inbox(id_inbox):
    print("id_inbox",id_inbox)
    for row in id_inbox:
        print("updated")
        try:
            cursor.execute("UPDATE tb_inbox SET flag='4' WHERE id_inbox='%s'" % row)
            connection.commit()
        except:
            print("Error Update")

if __name__ == '__main__':
    while True:
        # main()
        distribute_message()
        time.sleep(2)

