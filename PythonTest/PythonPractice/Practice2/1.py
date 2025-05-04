str = input()
len = len(str)
flag = True
for i in range(len//2):
    if str[i] != str[len-i-1]:
        flag = False
print(flag)