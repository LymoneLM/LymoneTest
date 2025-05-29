dict1 = {'赵广辉': '13299887777', '特朗普': '814666888', '普京': '522888666', '吴京': '13999887777'}
x = input()
y = input()
if x in dict1:
    print("您输入的姓名在通讯录中已存在" )
else:
    dict1[x]=y
    for i in dict1:
        print("{:s}:{:s}".format(i,dict1[i]))
