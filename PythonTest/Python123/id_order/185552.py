f = open(r"data.txt", "r")
n = f.read()
dict1 = {}
for i in n:
    if i in dict1:
        dict1[i]+=1
    else:
        dict1[i]=1
for i in sorted(dict1):
    print("{}:{:d}".format(i, dict1[i]))