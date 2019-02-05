from nlp import nlp
def main():
    msg = "om swastyastu, kapan galungan, kuningan, siwalatri, dewasa nikah tahun 2021"
    # msg.tolow
    tes=nlp()
    hasil=tes.get_reply(msg)

    for item in hasil:
        print(item)

if __name__== "__main__":
    main()