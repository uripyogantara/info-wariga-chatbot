from response import response


msg="Kapan galungan ?"

res =response()

result=res.get_response(msg)

for item in result:
    print(str(item))