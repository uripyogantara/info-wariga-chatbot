import re
import pymysql
from nltk.tokenize import MWETokenizer


msg=input()
msg=re.sub(r'[^\w]', ' ', msg)
tokenizer=MWETokenizer()
tokenizer.add_mwe(("buda","wage"))
token=tokenizer.tokenize(msg.split())

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='kalender_bali',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor=connection.cursor()

hari_raya={
    'kuningan':26,
    'galungan':19,
    'saraswati':42
}
# print(token)
def check_hari_raya(word):
    hari_raya=["galungan","kuningan","saraswati"]

    if word in hari_raya:
        return True
    else:
        return False

def check_bulan(word):
    bulan=["januari","februari","maret","april","mei","juni","juli","agustus"]
    if word in bulan:
        return True
    else:
        return False



responses=[]
entities={}
intent=None
response={}
for word in token:
    if check_hari_raya(word):
        if intent is not None:
            responses.append(response.copy())
            response={}
            entities={}
        intent='search_hari_raya'
        entities['hari_raya']=word

    if check_bulan(word):
        entities['bulan']=word
    response={
        'intent':intent,
        'entities':entities
    }

    # print(word,response)
responses.append(response.copy())
# print(responses)

for response in responses:
    # print(response)
    index=response['entities']['hari_raya']
    sql="CALL searchHariRaya(%s,2019)"%hari_raya[index]
    # print(sql)
    cursor.execute(sql)

    results=cursor.fetchall()

    for result in results:
        print(index+" : "+result['tanggal'].strftime("%Y-%m-%d"))


