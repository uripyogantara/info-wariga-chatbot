import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class connector:
    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="info_wariga",
                                                                          pool_reset_session=True,
                                                                          host='localhost',
                                                                          database='kalender_bali',
                                                                          user='root',
                                                                          password='')

        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_connection_object(self):
        connection_object = self.connection_pool.get_connection()
        return connection_object




