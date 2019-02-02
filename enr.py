import pymysql
import re
class Enr:
    _entities=[]

    def __init__(self):
        self.connection=pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='kalender_bali',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.connection.cursor()
        self.cursor.execute("SELECT * FROM tag")
        data = self.cursor.fetchall()

        self.set_entities(data=data)

        self.cursor.execute("SELECT * FROM basis_hari_raya")

        data = self.cursor.fetchall()

        self._basis_hari_raya = {}
        for item in data:
            self._basis_hari_raya[item["nama"]] = item["sql"]

        self.cursor.execute("SELECT * FROM padanan")

        data = self.cursor.fetchall()

        self._padanan = {}
        for item in data:
            self._padanan[item["value"]] = item["default"]

    def set_entities(self,data):
        entities={}
        for item in data:
            entities[item["word"]]=item["tag"]

        self._entities=entities

    def get_entities(self):
        return self._entities

    def get_basis_hari_raya(self):
        return self._basis_hari_raya

    def get_padanan(self,value):
        if value in self._padanan:
            return self._padanan[value]
        else:
            return value

    def get_reply(self,sql):
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        return data


