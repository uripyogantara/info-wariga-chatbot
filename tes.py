from nlp import nlp


def main():
    # number=100
    # for i in range(0,4):
    #     f=6
    #     if i==0:
    #         number=number*2
    #     number=number+f*i
    #     print(i,number)
    # number=number-4+1
    # print(number)
    msg = "/start"
    # msg.tolow
    tes=nlp()
    hasil=tes.get_reply(msg)
    #
    for item in hasil:
        print(item)
    print(msg)
#

if __name__== "__main__":
    main()