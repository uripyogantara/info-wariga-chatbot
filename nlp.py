from connector import connector
import re
from nltk.tokenize import MWETokenizer
from pprint import pprint

class nlp:
    def __init__(self):
        self.connection=connector().get_connection_object()
        self.cursor=self.connection.cursor(dictionary=True)
        self.cursor.execute("SELECT * FROM tag")
        data = self.cursor.fetchall()

        self.__set_entities(data=data)

        self.cursor.execute("SELECT * FROM basis_pengetahuan")

        data = self.cursor.fetchall()

        self._basis_pengetahuan = {}
        for item in data:
            self._basis_pengetahuan[item["nama"]] = item["sql"]

        self.cursor.execute("SELECT * FROM basis_pengetahuan_apa")

        data = self.cursor.fetchall()

        self._basis_pengetahuan_apa = {}
        for item in data:
            self._basis_pengetahuan_apa[item["nama"]] = item["deskripsi"]

        self.cursor.execute("SELECT * FROM padanan")

        data = self.cursor.fetchall()

        self._padanan = {}
        for item in data:
            self._padanan[item["value"]] = item["default"]


    def __set_entities(self,data):
        entities={}
        for item in data:
            # print(item)
            entities[item["word"]]=item["tag"]

        self._entities=entities

    def __tokenize(self,msg):
        msg = re.sub(r'[^\w]', ' ', msg)
        tokenizer = MWETokenizer()
        tokenizer.add_mwe(("buda", "wage"))
        token = tokenizer.tokenize(msg.split())
        return token

    def __get_enr(self,tokens):
        enr = {}
        for token in tokens:
            if token in self._entities:
                enr[token] = self._entities[token]
            elif re.match("\d{4}$", token):
                enr[token] = "tahun"
        return enr

    def __get_padanan(self,value):
        if value in self._padanan:
            return self._padanan[value]
        else:
            return value

    def __get_response(self,result):
        intent = None
        responses = []
        # for val in values:
        index = -1
        # response=
        responses.append(
            {
                "intent": intent,
                "entities": {}
            }
        )
        negation = False
        for key in result:
            val = result[key]
            if val == "when":
                intent = "search_when"

                # check apabila search_when ada di akhir maka seluruh intent yang None terupdate
                for item in responses:
                    if item["intent"] is None:
                        item["intent"] = intent
            elif val == "what":
                intent = "search_what"

                # check apabila search_when ada di akhir maka seluruh intent yang None terupdate
                for item in responses:
                    if item["intent"] is None:
                        item["intent"] = "search_what"
            elif val == "hari_raya":

                # apabila menemukan hari raya maka akan membuat array baru
                index += 1
                if (index >= len(responses)):
                    responses.append({
                        "intent": intent,
                        "entities": {}
                    })
                responses[index]["hari_raya"] = key
                negation = False
            elif val == "dewasa_ayu":

                # apabila menemukan hari raya maka akan membuat array baru
                index += 1
                if (index >= len(responses)):
                    responses.append({
                        "intent": intent,
                        "entities": {}
                    })
                responses[index]["dewasa_ayu"] = key
                negation = False
            elif val in ["negation"]:
                negation = True

            if val not in ["what", "when", "hari_raya", "dewasa_ayu", "negation"]:
                if val in responses[index]["entities"]:
                    responses[index]["entities"][val]["data"].append(key)
                else:
                    responses[index]["entities"][val] = {
                        "data": [key],
                        "negation": negation
                    }
        return responses

    def __result(self,responses):
        hasil = []

        for response in responses:
            if (response["intent"] == "search_when"):
                sql = "SELECT * FROM kalender WHERE tanggal>DATE(NOW())"

                if "hari_raya" in response:
                    sql += " and " + self._basis_pengetahuan[response["hari_raya"]]
                elif "dewasa_ayu" in response:
                    sql += " and " + self._basis_pengetahuan[response["dewasa_ayu"]]
                for entity in response["entities"]:
                    data = self.__join(response["entities"][entity]["data"])

                    if response["entities"][entity]["negation"]==True:
                        sql += " and %s not in (%s)" % (entity, data)
                    else:
                        sql += " and %s in (%s)" % (entity, data)
                print(sql)
                reply = self.__get_reply(sql)
                hasil.append(str(reply["tanggal"]))
            elif (response["intent"] == "search_what"):
                hari_raya = ""
                if "hari_raya" in response:
                    hari_raya=self._basis_pengetahuan_apa[response['hari_raya']]
                hasil.append(hari_raya)
                # print(response)

        return hasil

    def __join(self,data):
        sql = ""
        for i, item in enumerate(data):
            item = "'" + self.__get_padanan(item) + "'"
            if i < len(data) - 1:
                sql += item + ","
            else:
                sql += item
        return sql

    def __get_reply(self,sql):
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        self.connection.rollback()
        return data

    def get_reply(self,msg):
        token=self.__tokenize(msg)
        # print(token)
        enr = self.__get_enr(token)
        responses = self.__get_response(enr)

        # pprint(responses)
        result=self.__result(responses)
        return result


