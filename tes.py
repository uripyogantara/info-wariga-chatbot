from enr import Enr
from pprint import pprint
import re

from nltk.tokenize import MWETokenizer



# print(entities)
enr= Enr()
entities = enr.get_entities()
basis_hari_raya=enr.get_basis_hari_raya()
def get_enr(tokens):
    enr={}
    for token in tokens:
        if token in entities:
            enr[token]=entities[token]
        elif re.match("\d{4}$",token):
            enr[token]="tahun"
    return enr

def get_response(result):
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
    negation=False
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
            negation=False
        elif val == "dewasa_ayu":

            # apabila menemukan hari raya maka akan membuat array baru
            index += 1
            if (index >= len(responses)):
                responses.append({
                    "intent": intent,
                    "entities": {}
                })
            responses[index]["dewasa_ayu"] = key
            negation=False
        elif val in ["negation"]:
            negation=True

        if val not in ["what", "when","hari_raya","dewasa_ayu","negation"]:
            if val in responses[index]["entities"]:
                responses[index]["entities"][val]["data"].append(key)
            else:
                responses[index]["entities"][val]={
                    "data":[key],
                    "negation":negation
                }
    return responses

def result(responses):
    hasil = []
    for response in responses:
        if (response["intent"] == "search_when"):
            sql = "SELECT * FROM kalender WHERE tanggal>DATE(NOW())"

            if "hari_raya" in response:
                print("cari hari raya %s"%(response["hari_raya"]))
                sql+=" and "+basis_hari_raya[response["hari_raya"]]
            elif "dewasa_ayu" in response:
                print("cari dewasa %s"%(response["dewasa_ayu"]))
            for entity in response["entities"]:
                # if response["entities"][entity]["negation"]:

                data=join(response["entities"][entity]["data"])
                sql+=" and %s in (%s)"%(entity,data)
                # print(data)
                # print(response["entities"][entity])
            # print(sql)
            reply=enr.get_reply(sql)
            print(reply)
        elif (response["intent"] == "search_what"):
            hari_raya = ""
            for entity in response["entities"]:
                if response["entities"][entity] == "hari_raya":
                    hari_raya = entity
            hasil.append("kamu menanyakan apa %s" % hari_raya)
            print(response)

    return hasil

def join(data):
    sql=""
    for i,item in enumerate(data):
        item="'"+enr.get_padanan(item)+"'"
        if i<len(data)-1:
            sql+=item+","
        else:
            sql+=item
    return sql

def main():
    msg = "kapan siwalatri tahun 2021,2020 bukan senin selasa"
    msg = re.sub(r'[^\w]', ' ', msg)
    tokenizer = MWETokenizer()
    tokenizer.add_mwe(("buda", "wage"))
    token = tokenizer.tokenize(msg.split())
    enr = get_enr(token)
    responses=get_response(enr)
    result(responses)


if __name__== "__main__":
    main()