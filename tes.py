import nltk

import re
from nltk.tokenize import MWETokenizer,word_tokenize


msg="kapan galungan, kuningan"
msg=re.sub(r'[^\w]', ' ', msg)

tokenizer=MWETokenizer()
tokenizer.add_mwe(("buda","wage"))
token=tokenizer.tokenize(msg.split())

wtoken=word_tokenize(msg)
print(token)