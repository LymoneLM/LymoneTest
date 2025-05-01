a = 0
for i in range (1,967):
    if i%2==0:
        a-=i
    else:
        a+=i
print(a)