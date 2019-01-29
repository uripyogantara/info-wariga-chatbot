from enr import Enr
from pprint import pprint
import re

from nltk.tokenize import MWETokenizer

entities = Enr().get_entities()

# print(entities)

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

def main():
    msg = "kapan galungan juni juli 2019 bukan soma anggara , nikah januari maret wrespati jangan 2020 2025"
    msg = re.sub(r'[^\w]', ' ', msg)
    tokenizer = MWETokenizer()
    tokenizer.add_mwe(("buda", "wage"))
    token = tokenizer.tokenize(msg.split())
    enr = get_enr(token)

    # print(enr)

    response=get_response(enr)
    pprint(response)




if __name__== "__main__":
    main()