id = input()
if len(id) == 18:
    a = int(id[16])
    b = int(id[6:10])
    if a % 2 == 0:
        print('性别：女')
        if 2022 - b + 1 > 20:
            print('达到合法结婚年龄')
        else:
            print('未到合法结婚年龄')
    else:
        print('性别：男')
        if 2022 - b + 1 > 22:
            print('达到合法结婚年龄')
        else:
            print('未到合法结婚年龄')
else:
    print('身份证号错误')