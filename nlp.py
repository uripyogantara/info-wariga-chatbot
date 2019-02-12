from connector import connector
import re
from nltk.tokenize import MWETokenizer
from pprint import pprint
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


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

        self.cursor.execute("SELECT * FROM basis_pengetahuan_greeting")

        data = self.cursor.fetchall()

        self._basis_pengetahuan_greeting= {}
        for item in data:
            self._basis_pengetahuan_greeting[item["nama"]] = item["response"]

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

    def __stemming(self,msg):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        output = stemmer.stem(msg)

        return output

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
        bulan={
            'januari':'1',
            'februari':'2',
            'maret':'3',
            'april':'4',
            'mei':'5',
            'juni':'6',
            'juli':'7',
            'agustus':'8',
            'september': '9',
            'oktober': '10',
            'november': '11',
            'desember': '12',
        }
        if value in bulan:
            return bulan[value]
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
            elif val == "greeting":
                index+=1
                responses[index]["intent"]="greeting"
                responses[index]["greeting"] = key
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

            if val not in ["what", "when", "hari_raya", "dewasa_ayu", "negation","greeting"]:
                # print(responses[index]["intent"],key)
                if responses[len(responses)-1]["intent"]=="greeting":
                    print("append")
                    responses.append({
                        "intent": None,
                        "entities": {}
                    })
                    # print(responses)

                if val in responses[len(responses)-1]["entities"]:
                    responses[len(responses)-1]["entities"][val]["data"].append(key)
                else:
                    responses[len(responses)-1]["entities"][val] = {
                        "data": [key],
                        "negation": negation
                    }
        return responses

    def __result(self,responses):
        hasil = []

        for response in responses:
            if (response["intent"] == "search_when"):
                sql = "SELECT * FROM kalender WHERE tanggal>DATE(NOW())"

                data_wariga=None
                if "hari_raya" in response:
                    data_wariga=response["hari_raya"]
                    sql += " and " + self._basis_pengetahuan[response["hari_raya"]]
                elif "dewasa_ayu" in response:
                    data_wariga = "dewasa "+response["dewasa_ayu"]
                    sql += " and " + self._basis_pengetahuan[response["dewasa_ayu"]]
                for entity in response["entities"]:
                    data = self.__join(response["entities"][entity]["data"])

                    if response["entities"][entity]["negation"]==True:
                        sql += " and %s not in (%s)" % (entity, data)
                    else:
                        sql += " and %s in (%s)" % (entity, data)
                # print(sql)
                reply = self.__get_reply(sql)
                if data_wariga is None and not response["entities"]:
                    hasil.append("hmm aku ngga tau")
                elif reply is None:
                    hasil.append("sorry ya aku gak nemuin %s yang kamu cari"%data_wariga)
                else:
                    hasil.append(reply["tanggal"].strftime("%A, %d %B %Y"))
            elif (response["intent"] == "search_what"):
                hari_raya = ""
                if "hari_raya" in response:
                    hari_raya=self._basis_pengetahuan_apa[response['hari_raya']]
                hasil.append(hari_raya)
                # print(response)
            elif (response["intent"] == "greeting"):
                greeting=self._basis_pengetahuan_greeting[response['greeting']]
                # print(response["greeting"])
                hasil.append(greeting)

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

    def _padanan_kata(self,token):
        for key, value in enumerate(token):
            if value in self._padanan:
                token[key]= self._padanan[value]

    # def _get_response(self,):

    def get_reply(self,msg):
        # pprint(self._padanan)
        stemming=self.__stemming(msg)
        print(stemming)
        token=self.__tokenize(stemming)
        print(token)

        self._padanan_kata(token)

        pprint(token)
        enr = self.__get_enr(token)
        responses = self.__get_response(enr)

        pprint(responses)
        result=self.__result(responses)
        return result


