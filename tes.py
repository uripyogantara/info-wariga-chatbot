from nlp import nlp
import random
def main():
    msg = "kapan hari kemerdekaan"
    # msg.tolow
    tes=nlp()
    hasil=tes.get_reply(msg)

    for item in hasil:
        print(item)

if __name__== "__main__":
    # main()
    format=random.choice(responses["dewasa_ayu"])
    print(format.format("galungan","rabu"))


