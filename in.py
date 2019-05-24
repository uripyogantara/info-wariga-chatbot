import time
import mysql.connector

def checkMsg():
    cursor.execute("SELECT * FROM tb_outbox WHERE flag='1'")
    connection.rollback()

if __name__ == '__main__':
    connection = mysql.connector.connect( host='localhost',database='aaa',user='root',password='')
    cursor = connection.cursor(dictionary=True)
    while 1:
        try:
            checkMsg()
            time.sleep(1)
        except:
            connection.reconnect(attempts=1, delay=0)
