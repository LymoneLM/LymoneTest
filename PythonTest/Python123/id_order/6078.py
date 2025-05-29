x = input()
x = x.upper()
ctrl = x[0]
num = eval(x[1:])
if ctrl == 'C':
    print("F{:.2f}".format(num * 1.8 +32))
else:
    print("C{:.2f}".format((num-32)/1.8))