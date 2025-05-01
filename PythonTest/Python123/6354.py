x = input()
x = x.upper()
length = len(x)
y = eval(x[:length-1])
m = x[length-1]
if m == 'C':
    print("{:.2f}F".format(float(y * 1.8 + 32)))
elif m == 'F':
    print("{:.2f}C".format(float((y - 32) / 1.8)))
else:
    print("输入格式错误")