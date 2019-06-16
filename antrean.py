import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class antrean:
    def __init__(self,host):
        try:
            self.host=host
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

    def get_antrean(self):
        self.cursor.execute("SELECT * FROM tb_inbox WHERE flag IN('5')")
        antrean=self.cursor.fetchall()

        sql = "UPDATE tb_inbox SET flag='0' where flag IN ('5')"
        self.cursor.execute(sql)
        self.connection.commit()
        return antrean

    def distribute(self,antrean):
        id_inbox=[]
        self.cursor.execute("SELECT COUNT(*) as jumlah FROM tb_inbox WHERE flag IN('1','2','3')")
        result=self.cursor.fetchone()
        if result['jumlah']>= self.host['batas_atas']:
            print("server %d penuh"%self.host['id_host'])
        else:
            selisih=self.host['batas_atas']-result['jumlah']
            print("server %d kosong, %d buah"%(self.host['id_host'],selisih))
            for index,antrean_item in enumerate(antrean):
                if index<selisih:
                    sql = "INSERT INTO tb_inbox (chat_id, in_msg) VALUES (%s, %s)"
                    data=(
                        antrean_item["chat_id"],
                        antrean_item["in_msg"],
                    )

                    self.cursor.execute(sql,data)
                    self.connection.commit()
                    id_inbox.append(antrean_item['id_inbox'])
                else:
                    break
        self.connection.rollback()
        return id_inbox


    def __del__(self):
        self.cursor.close()
        self.connection.close()
        # print("closees")
