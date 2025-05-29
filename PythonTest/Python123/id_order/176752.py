list1 = (input()[1:-1].split(','))
list2 = []
for i in range(len(list1)):
    m = 1
    for t in range(len(list1)):
        if t != i:
            m *= int(list1[t])
    list2.append(m)
print(list2)
