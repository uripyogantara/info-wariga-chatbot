from enr import Enr
import re
from pprint import pprint
from nltk.tokenize import MWETokenizer
import pymysql

class response:
    def __init__(self):

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='kalender_bali',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        self._cursor = connection.cursor()

        self._cursor.execute("SELECT * FROM search_when")

        data=self._cursor.fetchall()

        self._search_when={}
        for item in data:
            self._search_when[item["entity"]]=item["sql"]
# print(search_when)

    def get_response(self,msg):
        # msg=msg.lo
        # msg="kapan galungan 2019, kuningan 2020, siwalatri hari sukra?"
        msg=re.sub(r'[^\w]', ' ', msg)
        tokenizer=MWETokenizer()
        tokenizer.add_mwe(("buda","wage"))
        token=tokenizer.tokenize(msg.split())

        enr=Enr(token=token)


        entities=enr.get_entities()
        result=enr.get_enr()

        intent=None
        responses=[]
        # for val in values:
        index=-1
        # response=
        responses.append(
            {
                "intent":intent,
                "entities":{}
            }
        )
        for key in result:
            val=result[key]
            if val=="when":
                intent="search_when"
                for item in responses:
                    if item["intent"] is None:
                        item["intent"]=intent
            elif val=="what":
                intent = "search_what"
                for item in responses:
                    if item["intent"] is None:
                        item["intent"]="search_what"
            elif val =="hari_raya":
                index+=1
                if(index>=len(responses)):
                    responses.append({
                        "intent":intent,
                        "entities":{}
                    })

            if val not in ["what","when"]:
                responses[index]["entities"][key]=val




        # pprint(responses)
        hasil=[]
        for response in responses:
            if(response["intent"]=="search_when"):
                sql="SELECT * FROM kalender WHERE tanggal>DATE(NOW())"
                first=True
                for entity in response["entities"]:
                    if response["entities"][entity]=="hari_raya":
                        sql_temp=self._search_when[entity]
                    else:
                        sql_temp=response["entities"][entity]+" = '"+entity+"'"

                    sql+=" AND "+sql_temp

                # print(sql)
                self._cursor.execute(sql)
                hasil.append(self._cursor.fetchone()["tanggal"])
            elif(response["intent"]=="search_what"):
                hari_raya=""
                for entity in response["entities"]:
                    if response["entities"][entity]=="hari_raya":
                        hari_raya=entity
                hasil.append("kamu menanyakan apa %s"%hari_raya)
                print(response)

        return hasil


        #

