import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class mojodomo:
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

    def get_antrean(self,antrean):
        self.cursor.execute("SELECT * FROM tb_inbox WHERE flag IN('4')")
        data=self.cursor.fetchall()

        for item in data:
            antrean.append(item)

        sql = "UPDATE tb_inbox SET flag='0' where flag IN ('4')"
        self.cursor.execute(sql)
        self.connection.commit()
        # return antrean

    def distribute(self,antrean):
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
                    # print("antrean item",antrean_item)
                    data=(
                        antrean_item["chat_id"],
                        antrean_item["in_msg"],
                    )

                    self.cursor.execute(sql,data)
                    self.connection.commit()
                    del antrean[index]
                    print(antrean)
                else:
                    break
        # return antrean
        # return result['jumlah']
        self.connection.rollback()

    # def distribute(self,antrean):


    def __del__(self):
        self.cursor.close()
        self.connection.close()
        # print("closees")
