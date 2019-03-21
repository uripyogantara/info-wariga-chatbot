from nlp import nlp


def main():
    msg = "Carikan saya dewasa ngaben"
    # msg.tolow
    tes=nlp()
    hasil=tes.get_reply(msg)

    for item in hasil:
        print(item)


if __name__== "__main__":
    main()