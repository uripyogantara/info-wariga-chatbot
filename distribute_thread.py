import threading
import time
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from antrean import antrean
exitFlag = 0

class antreanThread (threading.Thread):
    def __init__(self,host):
        threading.Thread.__init__(self)
        self.host=host
        try:
            connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mojodomo",
                                                                          pool_reset_session=True,
                                                                          host=host['ip'],
                                                                          database=host['nama_db'],
                                                                          user=host['user'],
                                                                          password=host['password'])

            self.connection=connection_pool.get_connection()
            self.cursor=self.connection.cursor(dictionary=True)

        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)
    def run(self):
        get_antrean(self.connection,self.cursor)
        self.cursor.close()
        self.connection.close()



def get_antrean(connection,cursor):
    cursor.execute("SELECT * FROM tb_antrean WHERE flag IN('1')")
    data_antrean = cursor.fetchall()
    # print(data_antrean)
    for host in hosts:
        data = antrean(host)
        id_antrean=data.distribute(data_antrean)
        # print(id_antrean)
        print(data_antrean)
        update_inbox(connection,cursor,id_antrean)

def update_inbox(connection, cursor, id_antrean):
    for row in id_antrean:
        try:
            cursor.execute("UPDATE tb_antrean SET flag='4' WHERE id_inbox='%s'" % row)
            connection.commit()
        except:
            print("Error Update")

master_con=mysql.connector.connect(host='localhost',database='mca_master_antrean',user='root',password='')
cursor_master=master_con.cursor(dictionary=True)

cursor_master.execute("SELECT * FROM master_antrean")
host_antrean=cursor_master.fetchall()

cursor_master.execute("SELECT * FROM master_host")
hosts=cursor_master.fetchall()

# print(hosts)
while 1:
    for host in host_antrean:
        # print(host)
        thread = antreanThread(host)
        thread.start()
    time.sleep(2)



