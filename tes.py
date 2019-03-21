from nlp import nlp


def main():
    msg = "dewasa nak nganten dong kak "
    # msg.tolow
    tes=nlp()
    hasil=tes.get_reply(msg)

    for item in hasil:
        print(item)


if __name__== "__main__":
    main()