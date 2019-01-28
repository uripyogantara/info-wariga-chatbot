import pymysql
import re
class Enr:
    _token=[]
    _entities=[]

    def __init__(self,token):
        connection=pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='kalender_bali',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        self._token=token
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

    def get_enr(self):
        enr={}
        for token in self._token:
            if token in self._entities:
                enr[token]=self._entities[token]
            elif re.match("\d{4}$",token):
                enr[token]="tahun"
        return enr



