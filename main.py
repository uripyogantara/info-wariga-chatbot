from enr import Enr
import re
from pprint import pprint
from nltk.tokenize import MWETokenizer

msg="kapan galungan, kuningan, siwalatri"
msg=re.sub(r'[^\w]', ' ', msg)
tokenizer=MWETokenizer()
tokenizer.add_mwe(("buda","wage"))
token=tokenizer.tokenize(msg.split())

enr=Enr(token=token)

entities=enr.get_entities()
result=enr.get_enr()

# pprint(result)
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
    # if val =="when":
    #     responses[0]["intent"]="search_when"
    # else:

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
    responses[index]["entities"][key]=val




pprint(responses)

#

