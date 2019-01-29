import pymysql
import re
class Enr:
    _entities=[]

    def __init__(self):
        connection=pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='kalender_bali',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM tag")
        data = cursor.fetchall()

        self.set_entities(data=data)

    def set_entities(self,data):
        entities={}
        for item in data:
            entities[item["word"]]=item["tag"]

        self._entities=entities

    def get_entities(self):
        return self._entities




