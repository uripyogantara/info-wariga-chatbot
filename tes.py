from reply import reply
def main():
    msg = "apa galungan, kapan kuningan 2020"

    rep=reply()
    hasil=rep.get_reply(msg)

    for item in hasil:
        print(item)

if __name__== "__main__":
    main()